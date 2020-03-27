from flask import render_template, request, url_for, redirect, jsonify, make_response
from flask_login import current_user, login_required
from werkzeug import secure_filename
import xlrd, csv
import json
import os

from app.secure import FILE_URL, UPLOAD_PATH, IP_HOST
from .base import web


@web.route('/upload/', methods=['GET','POST'])
def upload():
    # 上传首页
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
    # 上传2
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


@web.route('/uploads/<file_type>/', methods=['POST'])
def upload_file(file_type=None):
    # 上传文件并解析
    results = {'test': True, 'datas':[]}
    print(results, file_type)
    file_obj = request.files['files']
    if file_type == 'execl':
        wb = xlrd.open_workbook(file_contents=file_obj.read())
        table = wb.sheet_by_name('Sheet1')
        nrows, ncols = table.nrows, table.ncols
        for i in range(nrows):
            data = table.row_values(i)
            results['datas'].append(data)
    if file_type == 'csv':
        datas = file_obj.read().decode('utf-8')
        datas = datas.split('\r\n')
        results['datas'] = datas
    return make_response(jsonify(results), 200)

@web.route('/new_upload_html/', methods=['GET'])
def new_upload_html():
    return render_template('new_upload.html')

@web.route('/new_upload/', methods=['GET','POST'])
def new_upload():
    # filename/
    #     filename_type.json
    #     filename.type 文件
    #     filename_type1 文件子文件
    split_count = 10
    # 新的上传，可断点重传
    res = request
    root_path = UPLOAD_PATH
    if request.method == 'GET':
        # import pdb;pdb.set_trace()
        file_full_name = request.args['file_name']
        file_size = int(request.args['file_size'])
        last_time = request.args['last_time']
        split_count = request.args.get('split_count', split_count)
        *filename, file_type = file_full_name.split('.')
        file_name = '.'.join(filename)

        # /filename/filename_filetype.json
        # 查看当前文件所在目录是否有json文件
        file_dir = f'{root_path}{file_name}/'
        split_file_name = f'{file_name}_{file_type}'
        file_json = f'{file_dir}{split_file_name}.json'

        if os.path.exists(file_json):
            with open(file_json, 'r') as f:
                data = f.read()
            data = json.loads(data)
        else:
            data = {'name': file_name, 'type': file_type, 'size':file_size,
                'last_time': last_time, 'status': False, 'blocks':{}}
            block = int(file_size)//split_count
            blocks = {
                f'{split_file_name}.temp{i}': {'start': i*block, 'end': (i+1)*block, 'status': False}
                for i in range(split_count-1)
            }
            blocks[f'{split_file_name}.temp{split_count-1}'] = {'start': (split_count-1)*block, 'end': file_size, 'status': False}
            data['blocks'] = blocks
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            with open(file_json, 'w') as f:
                f.write(json.dumps(data))
        return make_response(jsonify(data), 200)
    else:
        # 查询后下载
        file_full_name = request.form['file_name']
        split_file_name = request.form['split_file_name']
        last_time = request.form['last_time']
        *filename, file_type = file_full_name.split('.')
        file_name = '.'.join(filename)

        # 查询文件是否修改
        file_dir = f'{root_path}{file_name}/'
        file_json_path = f'{file_dir}{file_name}_{file_type}.json'
        if not os.path.exists(file_json_path):
            return make_response('file_json_error', 400)

        with open(file_json_path, 'r') as f:
            file_json = json.loads(f.read())

        if file_json['last_time'] != last_time:
            return make_response('last_time_error', 400)

        # 上传文件并保存
        file = request.files['files']
        if file:
            file.save(os.path.join(f'{file_dir}', split_file_name))
            file_json['blocks'][split_file_name]['status'] = True
            with open(file_json_path, 'w') as f:
                f.write(json.dumps(file_json))

        # 检查文件是否全部更新,检查更新读取最新文件
        with open(file_json_path, 'r') as f:
            file_json = json.loads(f.read())

        for value in file_json['blocks'].values():
            if value['status'] == False:
                return make_response(jsonify(file_json), 200)

        # 全部上传，合并成一个
        data = b''
        for temp_file_name in file_json['blocks'].keys():
            temp_file_path = f'{file_dir}{temp_file_name}'
            with open(temp_file_path, 'rb') as f:
                data+=f.read()

        end_file_path = f'{file_dir}{file_name}.{file_type}'
        print(end_file_path)
        with open(end_file_path, 'wb') as  f:
            f.write(data)

        file_json['status'] = True
        with open(file_json_path, 'w') as f:
            f.write(json.dumps(file_json))
        return make_response(jsonify(file_json), 200)
