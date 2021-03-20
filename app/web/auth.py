# -*-coding = utf-8 -*-

# @Time: 2021/3/3 10:39
# @Author: bistro
# @File: auth.py
# @Software: PyCharm

from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required

from . import web
from ..forms.auth import RegisterForm, LoginForm, EmailForm, ReSetPasswordForm, ChangePasswordForm
from ..models.user import User
from ..models.base import db
from ..libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print(request.form)  # ImmutableMultiDict([])
    if request.method == 'POST':
        if form.validate():
            user = User()
            user.set_attrs(form.data)
            print(hasattr(user, 'password'))
            print(user.password)
            print(form.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('web.login'))
        else:
            flash(form.errors)
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print(session, bool(session))
    print(request.cookies)
    if request.method == 'POST' and form.validate():
        # session.permanent = True
        print(request.form)
        user = User.query.filter_by(email=form.email.data).first()
        print(user.verify_password(form.password.data))
        if user and user.verify_password(form.password.data):
            # 保存cookies
            login_user(user)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                return redirect(url_for('web.index'))
            return redirect(next_url)
        else:
            flash("用户名或者密码错误!!!")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first_or_404()
        send_mail(form.email.data, "重置你的密码", "email/reset_password.html", user=user, token=user.generate_token())
        flash('一封电子邮件发送至'+form.email.data+',请注意查收！')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ReSetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.password1.data, token)
        success = User.reset_password(form.password1.data, token)
        if success:
            flash('重置密码成功！')
            return redirect(url_for('web.login'))
        else:
            flash('重置密码失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route('/personal_center')
@login_required
def personal_center():
    return render_template('personal.html', user=current_user.summary)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(id=current_user.id).first()
        if user.verify_password(form.old_password.data):
            user.password = form.old_password.data
            print(user.password)
        else:
            flash('旧密码错误，请重新输入！')
            return redirect(url_for('web.change_password'))
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('修改密码成功！')
        return redirect(url_for('web.index'))
    return render_template('auth/change_password.html', form=form)
