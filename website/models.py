from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(100))
    Email=db.Column(db.String(100),unique=True)
    Password=db.Column(db.String(255))
    stu_db = db.relationship(
    'Student_db',
    backref='user',
    cascade="all, delete-orphan")

class Student_db(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Roll_No=db.Column(db.Integer,nullable=False)
    Name=db.Column(db.String(100),nullable=False)
    Age=db.Column(db.Integer)
    Class=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))





