from sqlalchemy import Column, Integer, DateTime, Boolean
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    status = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True, autoincrement=True)

    def set_attr(self, datas):
        for key, value in datas.items():
            if hasattr(self, key):
                value = value if value else None
                setattr(self, key, value)
        self.create_time = datetime.now()
        self.update_time = self.create_time
