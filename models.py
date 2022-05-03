from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
run_with_ngrok(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
db=SQLAlchemy(app)
class Student(db.Model):
    student_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number=db.Column(db.String(75), nullable=False, unique=True)
    first_name=db.Column(db.String(75), nullable=False)
    last_name=db.Column(db.String(75))

class Course(db.Model):
    course_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_code=db.Column(db.String(75), nullable=False, unique=True)
    course_name=db.Column(db.String(75), nullable=False)
    course_description=db.Column(db.String(75))


class Enrollments(db.Model):
    enrollment_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    estudent_id=db.Column(db.Integer, db.ForeignKey('student.student_id'),nullable=False)
    ecourse_id=db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
