from flask import current_app, flash, redirect, url_for, render_template

from . import web
from flask_login import login_required, current_user

from app.models.base import db
from ..libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from ..view_models.myTrades import MyTrades


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_list = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_list]
    print(isbn_list)
    wish_count = Gift.query_wish_count(isbn_list)
    print(wish_count)
    my_gifts = MyTrades(gifts_list, wish_count)
    return render_template('my_gifts.html', gifts=my_gifts.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        try:
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift, current_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        flash("已存在赠送清单或者心愿清单中，请勿重复添加！")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('该礼物正在交易当中，请先处理交易之后再进行操作！')
    else:
        gift.delete()
    try:
        db.session.add(gift)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('web.my_gifts'))
