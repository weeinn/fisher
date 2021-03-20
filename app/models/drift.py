# -*-coding = utf-8 -*-

# @Time: 2021/3/10 18:59
# @Author: bistro
# @File: drift.py
# @Software: PyCharm
from sqlalchemy import Column, String, Integer, SmallInteger

from app.models.base import Base
from ..libs.enums import PendingStatus

class Drift(Base):
    id = Column(Integer, primary_key=True)
    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    mobile = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(20))
    # 赠送者
    gifter_id = Column(Integer, nullable=False)
    gifter_nickname = Column(String(20), nullable=False)
    gift_id = Column(Integer, nullable=False)
    # 请求者信息
    requester_id = Column(Integer, nullable=False)
    requester_nickname = Column(String(20), nullable=False)
    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50), nullable=False)
    book_author = Column(String(30), nullable=False)
    book_img = Column(String(50), nullable=False)

    # 状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
