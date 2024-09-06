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
    
    classrooms = db.relationship('Classroom', backref='teacher', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='assigned_student', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='student_submission', lazy=True, cascade='all, delete-orphan')

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photo_url = db.Column(db.String(200))
    class_code = db.Column(db.String(10), unique=True, nullable=False)
    
    chapters = db.relationship('Chapter', backref='classroom', lazy=True, cascade='all, delete-orphan')

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with Assignment and Material
    assignments = db.relationship('Assignment', back_populates='chapter', cascade='all, delete-orphan')
    materials = db.relationship('Material', backref='chapter', lazy=True, cascade='all, delete-orphan')

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    file_url = db.Column(db.String(200), nullable=True)

    chapter = db.relationship('Chapter', back_populates='assignments')
    student = db.relationship('User', backref='student_assignments')

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    file_url = db.Column(db.String(200))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    file_url = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
