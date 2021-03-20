# -*-coding = utf-8 -*-

# @Time: 2021/3/3 11:10
# @Author: bistro
# @File: auth.py
# @Software: PyCharm
from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp

from app.models.user import User


class RegisterForm(Form):
    nickname = StringField(validators=[DataRequired(message='不能为空白字符，请重新输入'), Length(min=3, max=18,
                                                                                     message='昵称长度必须为3~18个字符')])
    email = StringField(validators=[DataRequired(message='不能为空白字符，请重新输入'), Email(message='邮箱格式不正确')])
    password = PasswordField(validators=[DataRequired(message='不能为空白字符，请重新输入'), Length(min=6, max=18,
                                                                                       message='密码长度必须为6~18个字符')])
    # 自定义验证器 validate_<fieldname>
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册！')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在！')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(message='请输入邮箱账号！'), Email()])
    password = PasswordField(validators=[DataRequired(message='请输入密码！'), Length(min=6, max=18)])

    # 自定义验证器 validate_<fieldname>
    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱不存在！')


class EmailForm(Form):
    email = StringField(validators=[DataRequired(message='请输入邮箱账号！'), Email(message='邮箱格式不正确!')])

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱还未注册用户！')


class ReSetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(message='请输入密码！'),
                                       Length(min=6, max=18),
                                       EqualTo('password2', message='密码不一致！')])
    password2 = PasswordField(validators=[DataRequired(message='请输入重复密码！'), Length(min=6, max=18)])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired(message='请输入旧密码！')])
    new_password1 = PasswordField(validators=[DataRequired(message='请输入新密码！'),
                                       Length(min=6, max=18),
                                       EqualTo('new_password2', message='密码不一致！')])
    new_password2 = PasswordField(validators=[DataRequired(message='请输入重复密码！'), Length(min=6, max=18)])


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(message='不能为空白字符，请重新输入'),
                                             Length(min=3, max=18, message='昵称长度必须为3~18个字符')])
    mobile = StringField(validators=[DataRequired(message='电话必须填写！'),
                                     Length(min=11, max=11), Regexp(r'1[3,4,5,7,8]\d{9}$', message='电话号码格式不正确')])
    address = StringField(validators=[DataRequired(message='地址必须填写！')])
    message = StringField()
