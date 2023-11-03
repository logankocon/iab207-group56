from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm, EditEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

#event blueprints
event_bp = Blueprint('event', __name__, url_prefix='/events')
#needed to make a new edits blueprint because for some reason having multiple sections in the url was breaking the styling
edit_bp = Blueprint('edit', __name__, url_prefix='/edit')

#displays event
@event_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    #checks if the event date has passed 
    if event.status == "Open" or "Sold Out":
      if datetime.date(datetime.now()) > event.event_date:
         event.status = "Inactive"
    form = CommentForm() 
    bookform = BookingForm()   
    return render_template('event_details.html', event=event, form=form, bookform=bookform)

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
#creates event
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
    image=db_file_path, event_date=form.date.data, max_tickets=form.tickets.data, tickets_left=form.tickets.data, location=form.location.data,
    artist=form.artist.data, time=form.time.data, genre=form.genre.data, user = current_user)
    print(form.name.data)
    db.session.add(event)
    db.session.commit()
    flash('Successfully created new event', 'success')
    return redirect(url_for('event.show', id = event.id))
  print(form.errors)
  return render_template('create_event.html', form=form)

@event_bp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
#adds a comment to event page
def comment(id):  
    form = CommentForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit()
      flash('Your comment has been added', 'success')  
    return redirect(url_for('event.show', id=id))

@event_bp.route('/<id>/book', methods=['GET', 'POST'])  
@login_required
#creates booking
def book(id):
   form = BookingForm()
   event = db.session.scalar(db.select(Event).where(Event.id==id))
   print(current_user)
   if form.validate_on_submit(): 
      #event can only be booked if status is open
      if event.status == "Open":
         if event.tickets_left >= int(form.tickets.data):
            booking = Booking(tickets=form.tickets.data, event = event,
                           user = current_user)
            db.session.add(booking) 
            event.tickets_left -= form.tickets.data
            if event.tickets_left <= 0:
               event.status = "Sold Out"
            db.session.commit()
            flash(f"New Booking with id {booking.id} created!")
         else:
            flash('Not enough available tickets', 'fail')
      else:
         flash('Event is not currently accepting bookings.')

     
      
   return redirect(url_for('event.show', id=id))

@edit_bp.route('/<id>', methods=['GET', 'POST'])
@login_required
#edits already existing booking
def edit(id):
  print('Method type: ', request.method)
  form = EditEventForm()
  event = db.session.scalar(db.select(Event).where(Event.id==id))
  #sets appropriate data in the forms
  form.description.data = event.description
  if event.status == "Cancelled":
     form.cancel.data = True
  if form.validate_on_submit():
    event.name = form.name.data
    event.description = form.description.data
    event.location = form.location.data
    event.artist = form.artist.data
    event.genre = form.genre.data
    event.event_date = form.date.data
    event.time = form.time.data
    event.tickets_left = form.tickets.data
    print(event.name)
    #a bunch of if statements to automatically set the event's status based on edits
    if str(form.image.data) == "None":
       db.session.commit()
    else:
       db_file_path = check_upload_file(form)
       event.image = db_file_path
       db.session.commit()
    if form.cancel.data == True:
       print("bunga1")
       event.status = "Cancelled"
    else:
       print("bunga")
       if event.status == "Cancelled":
         if datetime.date(datetime.now()) < event.event_date:
            if event.tickets_left <= 0:
               event.status = "Sold Out"
            else:
               event.status = "Open"
         else: 
            event.status = "Unavaliable"

    if event.status == "Unavaliable":
       if datetime.date(datetime.now()) < event.event_date:
         if event.tickets_left <= 0:
            event.status = "Sold Out"
         else:
            event.status = "Open"
    if event.status == "Sold Out":
       if event.tickets_left > 0:
            event.status = "Open"
    db.session.commit()
    flash('Successfully updated event', 'success')
   
    return redirect(url_for('edit.edit', id = id))
  return render_template('edit_event.html', form=form, event=event)

@event_bp.route('/booking_history')
@login_required
#renders user's booking history
def booking_history():
    bookings = db.session.scalars(db.select(Booking).where(Booking.user_id == current_user.id)).all()
    print(str(bookings))
    return render_template('booking_history.html', bookings = bookings)




def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path
