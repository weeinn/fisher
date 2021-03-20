# -*-coding = utf-8 -*-

# @Time: 2021/3/8 22:55
# @Author: bistro
# @File: email.py
# @Software: PyCharm
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print('网络超时')
            raise e


def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX']+subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to], reply_to=current_app.config['MAIL_USERNAME'])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
