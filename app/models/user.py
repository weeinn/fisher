# -*-coding = utf-8 -*-

# @Time: 2021/3/2 22:51
# @Author: bistro
# @File: user.py
# @Software: PyCharm
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float

from app import login_manager
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.libs.helper import is_isbn_or_key
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.enums import PendingStatus


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    __password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)  # 鱼豆
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    def get_id(self):
        return self.id

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pwd):
        self.__password = generate_password_hash(pwd)

    def verify_password(self, user_pwd):
        return check_password_hash(self.__password, user_pwd)

    def set_attrs(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def can_save_to_list(self, isbn):
        # 是否isbn--》isbn是否存在--》是否已经赠送过
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first_book:
            return False
        gift = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wish = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gift and not wish:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password( new_pwd, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        uid = data['id']
        user = User.query.get(uid)
        user.__password = generate_password_hash(new_pwd)
        print(user.__password)
        db.session.add(user)
        db.session.commit()
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_send = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        # TODO 两者都为0的情况
        return True if success_send >= success_receive*2 else False
        # return True if self.send_counter >= self.receive_counter*2 else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            receive_send=str(self.receive_counter)+'/'+str(self.send_counter)
        )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
