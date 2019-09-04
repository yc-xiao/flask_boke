from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import loginmanager
from app.models.base import BaseModel

class User(UserMixin, BaseModel):
    account = Column(String(length=32), nullable=False, unique=True)
    alias = Column(String(length=32))
    password = Column(String(length=100), nullable=False)
    email = Column(String(length=32), unique=True)
    image_url = Column(String(length=50))
    wx_open_id = Column(String(length=100))
    wx_name = Column(String(length=32))

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def set_attr(self, datas):
        super(User, self).set_attr(datas)
        self.alias = self.alias if self.alias else self.account

    # 配合login使用
    def get_id(self):
        return self.id

@loginmanager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
