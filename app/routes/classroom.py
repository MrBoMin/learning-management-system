from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required,current_user
from app.models import User,Classroom;
from app import db
from app.forms import LoginForm,ClassroomForm
from app.utils import save_image, generate_class_code,delete_file
import os


classroom = Blueprint('classroom',__name__)


@classroom.route('/')
@login_required
def index():
    classrooms = Classroom.query.filter_by(teacher_id=current_user.id).all()
    return render_template('index.html', classrooms=classrooms)


@classroom.route('/create-class', methods=['GET', 'POST'])
@login_required
def create_class():
    if current_user.role != 'teacher':
        flash('Only teachers can create classrooms.')
        return redirect(url_for('main.classroom.index'))

    form = ClassroomForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = save_image(form.photo.data, 'classroom_images')  
        
        classroom = Classroom(
            title=form.title.data,
            description=form.description.data,
            class_code=generate_class_code(),
            teacher_id=current_user.id,
            photo_url=filename  
        )
        db.session.add(classroom)
        db.session.commit()
        flash('Classroom created successfully!','success')
        return redirect(url_for('main.classroom.index'))

    return render_template('create_class.html', form=form)



@classroom.route('/delete_class/<int:id>',methods=['POST'])
@login_required
def delete_class(id):
    if current_user.role != 'teacher':
        flash('Only teachers can delete classrooms.')
        return redirect(url_for('main.classroom.index'))

    classroom = Classroom.query.filter_by(id=id,teacher_id=current_user.id).first() 

    if not classroom:
        flash('Classroom not found!')
        return redirect(url_for('main.classroom.index'))
    

    if classroom.photo_url:
        delete_file(os.path.join(classroom.photo_url))
    
    db.session.delete(classroom)
    db.session.commit()
    flash('Classroom deleted successfully!', 'success')
    return redirect(url_for('main.classroom.index'))



@classroom.route('/classrooms/<int:id>')
@login_required
def view_class(id):
    classroom = Classroom.query.filter_by(id = id).first()

    if not classroom:
        flash('Classroom not found!')
        return redirect(url_for('main.classroom.index'))
    
    return render_template('classroom.html') 




