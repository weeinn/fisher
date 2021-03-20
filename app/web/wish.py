from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from . import web
from .. import db
from ..models.wish import Wish
from ..view_models.myTrades import MyTrades


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_list = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_list]
    gifts_count = Wish.query_gift_count(isbn_list)
    my_wishes = MyTrades(wishes_list, gifts_count)
    print(my_wishes.trades)
    return render_template('my_wish.html', wishes=my_wishes.trades)


@web.route('/wishes/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        try:
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        flash("已存在赠送清单或者心愿清单中，请勿重复添加！")
    return redirect(url_for('web.book_detail', isbn=isbn))



