from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from . import web
from .. import db
from ..forms.auth import DriftForm
from ..libs.email import send_mail
from ..libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..view_models.book import BookViewModel
from ..view_models.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('不能请求索要自己的书籍！')
        return redirect(url_for('web.book_detail'))
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', user_beans=current_user.beans)
    gifter = current_gift.user.summary
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        flag = save_drift(form, current_gift)
        if flag:
            send_mail(current_gift.user.email, '有人想要你的书《'+current_gift.book['title']+'》',
                      'email/get_gift.html', wisher=current_user, gift=current_gift)
            return redirect(url_for('web.pending'))
        else:
            flash('数据保存出错')
            return render_template('404.html')
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/drift/pending')  # 待办的
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).all()
    drift_view = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=drift_view.data)


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 超权
    drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
    drift.pending = PendingStatus.Redraw
    current_user.beans += 1
    try:
        db.session.add(drift, current_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
    drift.pending = PendingStatus.Reject
    user = User.query.filter_by(id=drift.requester_id).first_or_404()
    user.beans += 1
    try:
        db.session.add(drift, user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
    drift.pending = PendingStatus.Success
    gift = Gift.query.filter_by(id=drift.gift_id, launched=False).first()
    gift.launched = True
    wish = Wish.query.filter_by(uid=drift.requester_id, isbn=drift.isbn, launched=False).first()
    wish.launched = True
    current_user.send_counter += 1
    wish_user = User.query.filter_by(id=drift.requester_id).first()
    wish_user.receive_counter += 1
    try:
        db.session.add(drift, gift)
        db.session.add(wish, current_user)
        db.session.add(wish_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('web.pending'))


@web.route('/satisfy_wish/<int:wid>')
def satisfy_wish(wid):
    wish = Wish.query.filter_by(id=wid).first_or_404()
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('您还没有上传该书籍，请先加入您的赠送清单之后，再进行赠送！')
    else:
        send_mail(wish.user.email, '有人想赠送你一本书', "email/satisify_wish.html", gift=gift, wish=wish)
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first_or_404()
    wish.delete()
    try:
        db.session.add(wish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('web.my_wish'))


def save_drift(form, current_gift):
    drift = Drift()
    form.populate_obj(drift)  # drift.message = form.message.data
    drift.gift_id = current_gift.id
    drift.gifter_id = current_gift.uid
    drift.gifter_nickname = current_gift.user.nickname
    drift.requester_id = current_user.id
    drift.requester_nickname = current_user.nickname
    book = BookViewModel(current_gift.book)
    drift.isbn = book.isbn
    drift.book_title = book.title
    drift.book_author = book.author
    drift.book_img = book.image
    current_user.beans -= 1
    try:
        db.session.add(drift, current_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True
