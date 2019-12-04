from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import ConnectionRefusedError
from flask_socketio import send, emit
from urllib import parse
import psutil
import random
import time

from .base import socketio

message_queue = []

@socketio.on('room')
def room(message):
    userid = current_user.get_id()
    userid = True
    current_user.alias = request.environ.get('HTTP_X_REAL_IP') or '127.0.0.1'
    if not userid:
        socketio.emit('room_reponse',
            {'message_queue': [], 'status':403, 'message': '要登录的!'}
        )
    message = parse.unquote(message)
    message_queue.append({'username': current_user.alias, 'message':message})
    queue = message_queue
    if len(message_queue) > 20:
        queue = message_queue[-20:]
    socketio.emit('room_reponse',
        {'message_queue': queue, 'status':200, 'message':'登录成功'}
    )

@socketio.on('system')
def background(message):
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        t = time.strftime('%M:%S', time.localtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        emit('server_response', {'data': [t, cpus], 'count': count})
        # socketio.emit('server_response', {'data': [t, cpus], 'count': count})
