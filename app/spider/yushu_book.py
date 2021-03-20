# -*-coding = utf-8 -*-

# @Time: 2021/2/19 15:58
# @Author: bistro
# @File: yushu_book.py
# @Software: PyCharm

from app.libs.httper import HTTP
from flask import current_app  # 本地代理


class YuShuBook:
    key_url = 'http://t.talelin.com/v2/book/search?q={}&count={}&start={}'  # 接口地址
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        data = HTTP.get(url)
        self.single_fill(data)

    def search_by_key(self, key, page=1):
        url = self.key_url.format(key, current_app.config['PER_PAGE'], self.calculate_start(page))
        print(url)
        data = HTTP.get(url)
        self.mutiple_fill(data)

    def calculate_start(self, page):
        return (page - 1)*current_app.config['PER_PAGE']

    def single_fill(self, data):
        if bool(data):
            self.total = 1
            self.books.append(data)

    def mutiple_fill(self, data):
        if bool(data):
            self.total = data['total']
            self.books = data['books']

    @property
    def first_book(self):
        return self.books[0] if self.total >= 1 else None
