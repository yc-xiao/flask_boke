from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required
from werkzeug import secure_filename
from app.secure import UPLOAD_FOLDER, FILE_URL
from .base import web
import os


@web.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['files']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(FILE_URL)
        return redirect(url_for('web.upload'))
