from . import db
import datetime
from sqlalchemy import DateTime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256),nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, name, email, phone,password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    heading = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow())

    def __init__(self, event,email, name, heading, description, created_date):
        self.event = event
        self.email = email
        self.name = name
        self.heading = heading
        self.description = description
        self.created_date = created_date

