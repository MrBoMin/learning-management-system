from werkzeug.utils import secure_filename
import os 
import uuid
from flask import current_app
import random
import string


def save_image(file,sub_dir='default'):
    random_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', sub_dir, random_filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)
    return f'{sub_dir}/{random_filename}'


def delete_file(file_path):
    abs_path = os.path.join(current_app.root_path, 'static/uploads', file_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False

def generate_class_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

