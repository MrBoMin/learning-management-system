from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required
from app.models import User;
from app import db
from app.forms import LoginForm,RegistrationForm
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError



auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.classroom.index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('main.auth.login'))

    return render_template('login.html', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    message = flash('Thanks for Using System', 'success')
    return redirect(url_for('main.auth.login'))




@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password=hashed_password, role=role)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.auth.login'))
        except IntegrityError as e:
            db.session.rollback()  
            if 'UNIQUE constraint failed: user.email' in str(e.orig):
                flash('Email already exists. Please use a different email address.', 'danger')
            else:
                flash('An unexpected error occurred. Please try again.', 'danger')

    return render_template('register.html', form=form)
