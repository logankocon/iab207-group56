from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm() 
    bookform = BookingForm()   
    return render_template('event_details.html', event=event, form=form, bookform=bookform)

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
    image=db_file_path,event_date=form.date.data, max_tickets=form.tickets.data, tickets_left=form.tickets.data, location=form.location.data,
    artist=form.artist.data, time=form.time.data, genre=form.genre.data)
    print("test2")
    print(form.name.data)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  else: 
    print("fail")
  return render_template('create_event.html', form=form)

@event_bp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event.id).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event_id=event,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))

@event_bp.route('/<id>/book', methods=['GET', 'POST'])  
@login_required
def book(id):
   form = BookingForm()
   event = db.session.scalar(db.select(Event.id).where(Event.id==id))
   img =  db.session.scalar(db.select(Event.image).where(Event.id==id))
   print(current_user)
   if form.validate_on_submit(): 
      booking = Booking(tickets=form.tickets.data, event_id=event, image=img,
                        user_id=current_user.id)
      db.session.add(booking) 
      db.session.commit() 
   return redirect(url_for('event.show', id=id))



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