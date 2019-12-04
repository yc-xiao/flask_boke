from flask import render_template, request, url_for, redirect
from .base import web

@web.route('/websocket/')
def websocket():
    return render_template('websocket.html')

@web.route('/room/')
def room():
    return render_template('room.html')

@web.route('/system/')
def system():
    return render_template('system.html')
