from flask import render_template, request, url_for, redirect
from .base import web

@web.route('/websocket/')
def websocket():
    return render_template('websocket.html')

@web.route('/websocket/1')
def websocket1():
    return render_template('websock_test.html')
