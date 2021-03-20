# -*-coding = utf-8 -*-

# @Time: 2021/3/7 13:09
# @Author: bistro
# @File: tradeInfo.py
# @Software: PyCharm
class TradeInfo:
    def __init__(self, goods):
        self.total = len(goods) if goods else 0
        self.trades = [self._single_good(good) for good in goods]

    def _single_good(self, good):
        if bool(good):
            if good.transform_datetime:
                time = good.transform_datetime.strftime("%Y-%m-%d")
            else:
                time = "未知"
            return dict(user_name=good.user.nickname, time=time, id=good.id)
        else:
            return {}

