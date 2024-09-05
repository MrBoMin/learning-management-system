from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required,current_user
from app.models import User,Classroom;
from app import db
from app.forms import LoginForm,ClassroomForm
from app.utils import save_image, generate_class_code


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
            filename = save_image(form.photo.data)  
        
        classroom = Classroom(
            title=form.title.data,
            description=form.description.data,
            class_code=form.class_code.data,
            teacher_id=current_user.id,
            photo_url=filename  
        )
        db.session.add(classroom)
        db.session.commit()
        flash('Classroom created successfully!','success')
        return redirect(url_for('main.classroom.index'))

    return render_template('create_class.html', form=form)



# @classroom.route('/join', methods = ['POST','GET'] )


