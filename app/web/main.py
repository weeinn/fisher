# -*-coding = utf-8 -*-

# @Time: 2021/3/6 20:30
# @Author: bistro
# @File: main.py
# @Software: PyCharm
from flask import render_template, redirect, url_for

from . import web
from ..models.gift import Gift
from ..view_models.book import BookViewModel


@web.route('/')
def transfer():
    return redirect(url_for('web.index'))


@web.route('/index')
def index():
    gifts = Gift.recent_upload()
    recent = [BookViewModel(gift.book) for gift in gifts]
    return render_template('index.html', recent=recent)

