# -*-coding = utf-8 -*-

# @Time: 2021/3/6 21:19
# @Author: bistro
# @File: wish.py
# @Software: PyCharm
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc, func

from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        return Wish.query.filter_by(uid=uid).order_by(desc(Wish.create_time)).all()

    @classmethod
    def query_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        # mysql 的 in 查询
        gifts_count = db.session.query(func.count(
            Gift.id), Gift.isbn).filter(
            Gift.launched == False, Gift.isbn.in_(isbn_list), Gift.status == 1).group_by(Gift.isbn).all()
        return Wish.handle_gift_data(gifts_count, isbn_list)

    @staticmethod
    def handle_gift_data(gifts_count, isbn_list):
        if not gifts_count:
            gifts_list = [{'isbn': isbn, 'count': 0} for isbn in isbn_list]
        else:
            gifts_list = []
            temp = {}
            for isbn in isbn_list:
                flag = False
                for gift in gifts_count:
                    if gift.isbn == isbn:
                        flag = True
                        temp = {'isbn': gift[1], 'count': gift[0]}
                if not flag:
                    temp = {'isbn': isbn, 'count': 0}
                gifts_list.append(temp)
        return gifts_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first_book
