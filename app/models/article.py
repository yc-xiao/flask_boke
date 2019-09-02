from sqlalchemy import Column, String, Integer, Text
from flask_sqlalchemy import SQLAlchemy
from app.models.base import BaseModel
# db = SQLAlchemy()

class Article(BaseModel):
    # id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text)
    writer_id = Column(Integer, nullable=False)
