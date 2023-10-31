from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
    image=db_file_path,event_date=form.date.data, max_tickets=form.tickets.data, tickets_left=form.tickets.data)
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