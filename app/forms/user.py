from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, \
EqualTo,ValidationError

from app.models.user import User

def check_account(form, field):
    if User.query.filter(User.account==field.data).first():
        raise ValidationError('账号已被注册')

class RegisterForm(Form):
    account = StringField(validators=[
        DataRequired(message='账号不为空'),
        Length(min=2, max=20, message='账号长度在2-20之间'),
        check_account
    ])
    password1 = PasswordField(validators=[
        DataRequired(message='密码不为空'),
        Length(min=6, max=30, message='密码长度在6-30之间')
    ])
    password2 = PasswordField(validators=[
        EqualTo('password1', message='两次密码不一样')
    ])
    alias = StringField(validators=[
        Length(max=20, message='名称最大长度为20之间')
    ])
    email = StringField()

    def validate_email(self, field):
        # 自定义邮箱验证，若邮箱为非空，则实例化Email验证邮箱。
        if len(field.data):
            email = Email(message='邮箱格式不对')
            email(self, field)
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')


class LoginForm(Form):
    account = StringField(validators=[
        DataRequired(message='账号不为空'),
        Length(min=2, max=20, message='账号长度在2-20之间')
    ])
    password = PasswordField(validators=[
        DataRequired(message='密码不为空'),
        Length(min=6, max=30, message='密码长度在6-30之间')
    ])
