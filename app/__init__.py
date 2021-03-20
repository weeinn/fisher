# -*-coding = utf-8 -*-

# @Time: 2021/2/20 21:53
# @Author: bistro
# @File: __init__.py
# @Software: PyCharm

from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    # print(__name__)  # print app
    app.config.from_pyfile("config\\secure.py")
    app.config.from_pyfile("config\\setting.py")
    register_blueprint(app)
    db.init_app(app)
    login_manager.login_view = 'web.login'  # 需要登录时，默认跳转
    login_manager.init_app(app)
    mail.init_app(app)
    # db.drop_all(app=app)
    # db.create_all(app=app)
    return app


def register_blueprint(app):  # 这是自己定义的注册蓝图的方法
    from app.web import web
    app.register_blueprint(web)  # 这是Flask核心对象app自带的注册蓝图方法
    return app

