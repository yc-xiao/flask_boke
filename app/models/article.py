from sqlalchemy import Column, String, Integer, Text
from app.models.base import BaseModel

class Article(BaseModel):
    title = Column(String(50), nullable=False)
    content = Column(Text)
    writer_id = Column(Integer, nullable=False)
    writer_alias = Column(String(length=32), nullable=False)
