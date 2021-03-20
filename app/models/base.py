# -*-coding = utf-8 -*-

# @Time: 2021/3/3 10:04
# @Author: bistro
# @File: base.py
# @Software: PyCharm
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class customizeQuery(BaseQuery):  # 改写filter_by
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1
        return super().filter_by(**kwargs)


db = SQLAlchemy(query_class=customizeQuery)  # 关系型数据库框架 ORM


class Base(db.Model):
    __abstract__ = True  # 设置该参数，表示再创建模型的时候不会创建该表
    create_time = Column(Integer)  # 实现软删除，假删除
    status = Column(SmallInteger, default=1)  # 实现软删除，假删除

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())  # 获取当前的时间戳

    @property
    def transform_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
