from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user

from app.forms.user import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db
from .base import web

@web.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', form=form.data)
    if form.validate():
        user = User()
        user.set_attr(form.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    else:
        for error in form.errors.values():
            flash('_'.join(error))
        return render_template('register.html', form=form.data)

@web.route('/forget_password', methods=['GET','POST'])
def forget_password():
    return render_template('forget_password.html')

@web.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(account=form.account.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # 这里没有跳转得原因是因为url='/login'
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误!!')
    return render_template('login.html', form=form)

@web.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('web.index'))
