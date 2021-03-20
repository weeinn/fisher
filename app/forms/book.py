# -*-coding = utf-8 -*-

# @Time: 2021/2/22 16:15
# @Author: bistro
# @File: book.py
# @Software: PyCharm
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, DataRequired, NumberRange


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30), DataRequired(message='需要非空字符')])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
