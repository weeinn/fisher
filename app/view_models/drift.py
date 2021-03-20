# -*-coding = utf-8 -*-

# @Time: 2021/3/12 17:44
# @Author: bistro
# @File: drift.py
# @Software: PyCharm
from app.libs.enums import PendingStatus


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}
        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        you_are = ''
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        if drift.gifter_id == current_user_id:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        status_str = PendingStatus.pending_str(drift.pending, you_are)
        drift = {
            'book_img': drift.book_img,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'drift_id': drift.id,
            'recipient_name': drift.recipient_name,
            'address': drift.address,
            'mobile': drift.mobile,
            'message': drift.message,
            'status': drift.pending,
            'you_are': you_are,
            'operator': drift.gifter_nickname if you_are == 'requester' else drift.requester_nickname,
            'status_str': status_str,
            'date': drift.transform_datetime.strftime("%Y-%m-%d")
        }
        return drift


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)
