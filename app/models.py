from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(30), nullable=False) 
    classrooms = db.relationship('Classroom', backref='teacher', lazy=True)
    assignments = db.relationship('Assignment', backref='student', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photo_url = db.Column(db.String(200))
    class_code = db.Column(db.String(10), unique=True, nullable=False)  # New column for class code
    assignments = db.relationship('Assignment', backref='classroom', lazy=True)
    materials = db.relationship('Material', backref='classroom', lazy=True)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    due_date = db.Column(db.DateTime)
    file_url = db.Column(db.String(200))

    submissions = db.relationship('Submission', backref='assignment', lazy=True)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    file_url = db.Column(db.String(200))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    file_url = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
