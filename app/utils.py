from werkzeug.utils import secure_filename
import os 
from flask import current_app
import random
import string


def save_image(image_file):
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(current_app.root_path, 'static/uploads', filename)
    image_file.save(filepath)
    return filename

def generate_class_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

