from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import ConnectionRefusedError
from flask_socketio import send, emit
import psutil
import random
import time

from .base import socketio

message_queue = []

@socketio.on('room')
def room(message):
    userid = current_user.get_id()
    if not userid:
        socketio.emit('room_reponse',
            {'message_queue': [], 'status':403, 'message': '要登录的!'}
        )
    message_queue.append({'username': current_user.alias, 'message':message})
    socketio.emit('room_reponse',
        {'message_queue': message_queue, 'status':200, 'message':'登录成功'}
    )

@socketio.on('system')
def background(message):
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        t = time.strftime('%M:%S', time.localtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        socketio.emit('server_response', {'data': [t, cpus], 'count': count})
