# database models 
# the dot means from this package so anythin within __init__
from enum import unique
from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default = 'client')
    pets = db.relationship('Pet', backref='owner')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vaccinations = db.relationship('Vaccination', backref='pet')
    appointments = db.relationship('Appointment', backref='pet')


class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    date = db.Column(db.String(20))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

# need to commit admin personnel to the database manually
