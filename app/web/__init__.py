# -*-coding = utf-8 -*-

# @Time: 2021/2/20 21:53
# @Author: bistro
# @File: __init__.py
# @Software: PyCharm
from flask import Blueprint, render_template

web = Blueprint('web', __name__)  # 注册蓝图 第一个参数name蓝图名称 第二个import_name:用来定位蓝图的根路径


@web.app_errorhandler(404)  # 底层还是调用的app.errorhandler(code)方法
def not_found(e):
    return render_template('404.html'), 404


from app.web import book
from app.web import drift
from app.web import gift
from app.web import wish
from app.web import auth
from app.web import main


