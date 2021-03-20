# -*-coding = utf-8 -*-

# @Time: 2021/2/22 17:25
# @Author: bistro
# @File: book.py
# @Software: PyCharm
from sqlalchemy import Column, Integer, String  # Code First  Model First Database First
from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    summary = Column(String(1000))  # 描述
    isbn = Column(String(15), nullable=False, unique=True)
    price = Column(String(20))
    binding = Column(String(20))  # 帧装
    pages = Column(Integer)
    pubdate = Column(String(20))
    publisher = Column(String(50))
    image = Column(String(50))  # 链接
