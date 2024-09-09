from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required,current_user
from app.models import User,Classroom,Chapter,Material,Assignment
from app import db
from app.forms import LoginForm,ClassroomForm,ChapterForm,MaterialForm,AssignmentForm
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



@classroom.route('/classrooms/<int:id>', methods=['GET'])
@login_required
def view_class(id):
    classroom = Classroom.query.get_or_404(id)
    
    chapters = Chapter.query.filter_by(classroom_id=id).all()
    
    chapters_with_content = []
    for chapter in chapters:
        materials = Material.query.filter_by(chapter_id=chapter.id).all()
        assignments = Assignment.query.filter_by(chapter_id=chapter.id).all() 
        chapters_with_content.append({'chapter': chapter, 'materials': materials, 'assignments': assignments})

    
    return render_template('classroom.html', classroom=classroom, chapters=chapters_with_content)

@classroom.route('/classrooms/<int:id>/add-chapter', methods=['GET', 'POST'])
@login_required
def add_chapter(id):
    form = ChapterForm()
    classroom = Classroom.query.get_or_404(id)
    
    if form.validate_on_submit():
        new_chapter = Chapter(
            title=form.title.data,
            description=form.description.data,
            classroom_id=id
        )
        db.session.add(new_chapter)
        db.session.commit()
        flash('New chapter added successfully!', 'success')
        return redirect(url_for('main.classroom.view_class', id=id))
    
    return render_template('create_chapter.html', form=form, classroom=classroom)



@classroom.route('/classrooms/<int:classroom_id>/chapter/<int:chapter_id>/add-material', methods = ['GET','POST'])
@login_required
def add_material(classroom_id,chapter_id):
    form = MaterialForm() 
    chapter = Chapter.query.get_or_404(chapter_id)
    if form.validate_on_submit():
        file_url = None 
        if form.file.data:
            file_url = save_image(form.file.data,'materials')


        material = Material(
            title = form.title.data,
            content = form.content.data, 
            chapter_id = chapter_id, 
            file_url = file_url
        ) 


        db.session.add(material) 
        db.session.commit() 
        flash('New Material is added successfully.','success')
        return redirect(url_for('main.classroom.view_class', id = classroom_id))
    
    return render_template('create_material.html', form =form, chapter = chapter)



@classroom.route('/material/<int:material_id>', methods=['GET'])
@login_required
def view_material(material_id):
    material = Material.query.get_or_404(material_id)
    return render_template('material.html', material=material) 


@classroom.route('/classrooms/<int:classroom_id>/chapter/<int:chapter_id>/add-assignment', methods=['GET', 'POST'])
@login_required
def add_assignment(classroom_id, chapter_id):
    form = AssignmentForm()
    chapter = Chapter.query.get_or_404(chapter_id)

    if current_user.role != 'teacher':
        flash('Only teachers can create assignments.', 'warning')
        return redirect(url_for('classroom.view_class', id=classroom_id))

    if form.validate_on_submit():
        file_url = None
        if form.file.data:
            file_url = save_image(form.file.data, 'assignments') 

        new_assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            chapter_id=chapter_id,
            teacher_id=current_user.id,  
            file_url=file_url
        )
        db.session.add(new_assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('main.classroom.view_class', id=classroom_id))

    return render_template('create_assginment.html', form=form, chapter=chapter)


@classroom.route('/assignment/<int:assignment_id>', methods=['GET'])
@login_required
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    return render_template('assignment.html', assignment=assignment) 
