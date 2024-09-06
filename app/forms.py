from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email, Length, EqualTo
from wtforms import SelectField,StringField, PasswordField, SubmitField,FileField
from flask_wtf.file import FileAllowed, FileRequired



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])

    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')



class ClassroomForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])  # Optional description
    #class_code = StringField('Class Code', validators=[DataRequired(), Length(min=6, max=10)])  # Class code field
    photo = FileField('Classroom Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])  # Image upload field
    submit = SubmitField('Create Classroom')


