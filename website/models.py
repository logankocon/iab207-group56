from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum


class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    location = db.Column(db.String(400))
    time = db.Column(db.String(400))
    artist = db.Column(db.String(400))
    genre = db.Column(db.String(400))
    event_date = db.Column(db.String(400))
    #db.DateTime, default=datetime.now()
    max_tickets = db.Column(db.Integer)
    tickets_left = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(Enum('Open', 'Sold Out', 'Cancelled', 'Unavaliable'), default='Open')


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable = False)
    purchase_date = db.Column(db.DateTime, default = datetime.now())

    user = db.relationship('User', backref='bookings')
    event = db.relationship('Event', backref='bookings')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())

    #fk's
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
