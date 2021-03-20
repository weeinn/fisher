# -*-coding = utf-8 -*-

# @Time: 2021/3/3 9:44
# @Author: bistro
# @File: myTrades.py
# @Software: PyCharm
from flask import current_app
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc, func

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def recent_upload(cls):
        gifts = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_UPLOAD_COUNT']).distinct().all()
        return gifts

    @classmethod
    def get_user_gifts(cls, uid):
        return Gift.query.filter_by(uid=uid).order_by(desc(Gift.create_time)).all()

    @classmethod
    def query_wish_count(cls, isbn_list):
        from app.models.wish import Wish
        # mysql 的 in 查询
        wish_count = db.session.query(func.count(
            Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(Wish.isbn).all()
        return Gift.handle_wish_data(wish_count, isbn_list)

    @staticmethod
    def handle_wish_data(wish_count, isbn_list):
        if not wish_count:
            wishes_list = [{'isbn': isbn, 'count': 0} for isbn in isbn_list]
        else:
            wishes_list = []
            temp = {}
            for isbn in isbn_list:
                flag = False
                for wish in wish_count:
                    if wish.isbn == isbn:
                        flag = True
                        temp = {'isbn': wish[1], 'count': wish[0]}
                if not flag:
                    temp = {'isbn': isbn, 'count': 0}
                wishes_list.append(temp)
        return wishes_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first_book

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

