from sqlalchemy.sql import func
from sqlalchemy.dialects import mysql
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    sender_id = db.Column(db.String(20), db.ForeignKey('user.id'), primary_key=True) 
    #date = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    date = db.Column(db.String(30), primary_key=True)
    content_text = db.Column(db.String(10000))

class LoggedIn(db.Model):
    active_id = db.Column(db.String(20), db.ForeignKey('user.id'), primary_key=True)
    #date_in = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    #date_out = db.Column(db.DateTime(timezone=True), nullable=True)
    date_in = db.Column(db.String(30), primary_key=True)
    date_out = db.Column(db.String(30), nullable=True)
