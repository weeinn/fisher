# -*-coding = utf-8 -*-

# @Time: 2021/2/28 10:31
# @Author: bistro
# @File: book.py
# @Software: PyCharm
# 介于view 和 model 之间的一层处理
class BookViewModel:
    def __init__(self, data):  # 原始数据
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.publisher = data['publisher']
        self.price = data['price']
        self.image = data['image']
        self.summary = data['summary'] or ''
        self.isbn = data['isbn']
        self.pages = data['pages'] or '不详'
        self.pubdate = data['pubdate']
        self.binding = data['binding'] or '未知'

    @property
    def generate_introduction(self):
        """
        通过过滤器进行介绍信息的拼接
        :return: string introduction
        """
        introduction = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(introduction)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.keyword = ''
        self.books = []

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]