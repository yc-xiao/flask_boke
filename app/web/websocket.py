from flask import render_template, request, url_for, redirect
from flask_socketio import send, emit
from random import randint

from .base import web

@web.route('/websocket/')
def websocket():
    return render_template('websocket.html')

@web.route('/room/')
def websocket_room():
    return render_template('room.html')

@web.route('/system/')
def websocket_system():
    return render_template('system.html')

@web.route('/signal/')
def websocket_signal():
    # emit('前台监听事件', '发送信息', )
    # namespace 名称空间允许客户端在同一物理套接字上多路复用多个独立的连接
    # https://flask-socketio.readthedocs.io/en/latest/具体
    data = {
        'message_queue': [{'username': 'test', 'message': '广播测试'}],
        'status':200,
        'message':'登录成功'
    }
    emit('room_reponse', data, broadcast=True, namespace='/')
    return ''

# @web.route('/sub/')
# def websocket_sub():
#     num = randint(0,1000)
#     # 如果不是广播需要指定sid
#     emit('sub_response', num, namespace='/')
#     return '广播一下'

@web.route('/subs/')
def websocket_subs():
    num = randint(0,1000)
    # 全体广播
    emit('sub_response', num, broadcast=True, namespace='/')
    return '广播一下'

# @web.route('/sub/<string:name>')
# def websocket_sub_name(name):
#     num = randint(0,1000)
#     # 指定命名空间广播, 如果不是广播需要指定sid
#     emit('sub_response', num, namespace=f'/{name}')
#     return '广播一下'

@web.route('/subs/<string:name>')
def websocket_subs_name(name):
    num = randint(0,1000)
    # 指定命名空间广播
    emit('sub_response', num, broadcast=True, namespace=f'/{name}')
    return '广播一下'
