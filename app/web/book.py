# -*-coding = utf-8 -*-

# @Time: 2021/2/20 21:27
# @Author: bistro
# @File: book.py
# @Software: PyCharm
import json

from flask import jsonify, request, render_template, flash  # 消息闪现
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web
from app.forms.book import SearchForm
from app.view_models.book import BookCollection, BookViewModel
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.tradeInfo import TradeInfo


@web.route("/book/search")
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        key_or_isbn = is_isbn_or_key(q)
        print(key_or_isbn)
        yushu_book = YuShuBook()
        if key_or_isbn == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_key(q, page)
        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        # return jsonify(form.errors)
        flash("搜索的关键字不合法，请重新输入！")

    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False  # 是否在赠送清单
    has_in_wishes = False   # 是否在心愿清单
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first_book)
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True
    gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = TradeInfo(gifts)
    trade_wishes = TradeInfo(wishes)
    return render_template('book_detail.html', book=book, wishes=trade_wishes, gifts=trade_gifts,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
