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

@classroom.route('/classrooms')
@login_required
def show_classrooms():
    return redirect(url_for('main.classroom.index'))


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
    chapter = Chapter.query.get_or_404(material.chapter_id)
    classroom = Classroom.query.get_or_404(chapter.classroom_id)
    
    return render_template('material.html', material=material, chapter=chapter, classroom=classroom)


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



@classroom.route('/classrooms/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    classroom = Classroom.query.get_or_404(id)

    if current_user.role != 'teacher' or classroom.teacher_id != current_user.id:
        flash('Only the teacher can edit this classroom.', 'warning')
        return redirect(url_for('main.classroom.view_class', id=id))

    form = ClassroomForm(obj=classroom)

    if form.validate_on_submit():
        if form.photo.data:
            if classroom.photo_url:
                delete_file(os.path.join(classroom.photo_url)) 
            classroom.photo_url = save_image(form.photo.data, 'classroom_images')

        classroom.title = form.title.data
        classroom.description = form.description.data
        db.session.commit()
        flash('Classroom updated successfully!', 'success')
        return redirect(url_for('main.classroom.view_class', id=id))

    return render_template('edit_class.html', form=form, classroom=classroom)



@classroom.route('/classrooms/<int:classroom_id>/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_chapter(classroom_id, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if current_user.role != 'teacher':
        flash('Only teachers can edit this chapter.', 'warning')
        return redirect(url_for('main.classroom.view_class', id=classroom_id))

    form = ChapterForm(obj=chapter)

    if form.validate_on_submit():
        chapter.title = form.title.data
        chapter.description = form.description.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('main.classroom.view_class', id=classroom_id))

    return render_template('edit_chapter.html', form=form, chapter=chapter)


@classroom.route('/classrooms/<int:classroom_id>/chapter/<int:chapter_id>/material/<int:material_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_material(classroom_id, chapter_id, material_id):
    material = Material.query.get_or_404(material_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    classroom = Classroom.query.get_or_404(classroom_id)

    if current_user.role != 'teacher':
        flash('Only teachers can edit this material.', 'warning')
        return redirect(url_for('main.classroom.view_class', id=classroom_id))

    form = MaterialForm(obj=material)

    if form.validate_on_submit():
        if form.file.data:
            if material.file_url:
                delete_file(os.path.join(material.file_url))  
            material.file_url = save_image(form.file.data, 'materials')

        material.title = form.title.data
        material.content = form.content.data
        db.session.commit()
        flash('Material updated successfully!', 'success')
        return redirect(url_for('main.classroom.view_class', id=classroom_id))

    return render_template('edit_material.html', form=form, material=material, chapter=chapter, classroom=classroom)

