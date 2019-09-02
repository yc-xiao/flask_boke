from sqlalchemy import Column, Integer, SmallInteger
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())
