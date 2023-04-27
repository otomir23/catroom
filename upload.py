import os
import uuid
from typing import Optional

from flask import send_from_directory, Flask
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')


def upload_file(file: FileStorage) -> Optional[str]:
    """Validates file and saves it under a new name

    :param file: file to upload
    :return: new filename
    """
    filename = secure_filename(file.filename)
    extension = '' if '.' not in filename else filename.rsplit('.', 1)[1].lower()
    if extension in ALLOWED_EXTENSIONS:
        new_filename = f"{str(uuid.uuid4())}.{extension}"
        file.save(os.path.join(UPLOAD_FOLDER, new_filename))
        return new_filename


def setup_app_uploads(app: Flask):
    """Set up the uploads folder for the app.

    :param app: app to set up the uploads folder for"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 megabytes

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
