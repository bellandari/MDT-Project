from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    notes = db.relationship('Note')

class Ped(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    dob = db.Column(db.String(8))
    drivers = db.Column(db.String(15))
    fishing = db.Column(db.String(15))
    hunting = db.Column(db.String(15))
    gun = db.Column(db.String(15))
    warrant = db.Column(db.String(150))
    history = db.Column(db.String(10000))