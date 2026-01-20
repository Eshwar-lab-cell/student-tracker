from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
