from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required
from werkzeug import secure_filename
import os

from app.secure import FILE_URL, UPLOAD_PATH, IP_HOST
from .base import web


@web.route('/upload/', methods=['GET','POST'])
def upload():
    url = request.url
    url = url.replace('http://localhost:5000', IP_HOST)
    # url = url.replace('localhost:5000', IP_HOST)
    if request.method == 'GET':
        files = os.listdir(UPLOAD_PATH)
        temp_files = []
        temp_f_files, temp_d_files = [], []
        for file in files:
            path = UPLOAD_PATH + file
            if os.path.isfile(path):
                temp_f_files.append({'url':f'{FILE_URL}{file}', 'name': file})
            else:
                temp_d_files.append({'url':f'{url}{file}/', 'name': f'{file}/'})
            temp_files = temp_d_files + temp_f_files
        return render_template('upload.html', upload_url=url, files=temp_files)
    if request.method == 'POST':
        file = request.files['files']
        if file:
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(UPLOAD_PATH, filename))
            return redirect(url_for('web.upload'))
        return redirect(url_for('web.upload'))

@web.route('/upload/<path:file_path>', methods=['GET','POST'])
def upload2(file_path=None):
    url = request.url
    url = url.replace('http://localhost:5000', IP_HOST)
    # url = url.replace('localhost:5000', IP_HOST)
    if request.method == 'GET':
        upload_path = UPLOAD_PATH + file_path
        files = os.listdir(upload_path)
        temp_files = []
        temp_f_files, temp_d_files = [], []
        for file in files:
            path = upload_path + file
            if os.path.isfile(path):
                temp_f_files.append({'url':f'{FILE_URL}{file_path}{file}', 'name': file})
            else:
                temp_d_files.append({'url':f'{url}{file}/', 'name': f'{file}/'})
            temp_files = temp_d_files + temp_f_files
        return render_template('upload.html', upload_url=url, files=temp_files)

    if request.method == 'POST':
        file = request.files['files']
        if file:
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(f'{UPLOAD_PATH}/{file_path}', filename))
            return redirect(url)
        return redirect(url_for('web.upload'))
