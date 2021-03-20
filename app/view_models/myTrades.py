# -*-coding = utf-8 -*-

# @Time: 2021/3/7 21:00
# @Author: bistro
# @File: myTrades.py
# @Software: PyCharm
from app.view_models.book import BookViewModel


class MyTrades:
    def __init__(self, trades_list, count_list):
        self.trades = []
        self.trades_list = trades_list
        self.count_list = count_list
        self.__fill()

    def __fill(self):
        for trade in self.trades_list:
            for trade_count in self.count_list:
                if trade.isbn == trade_count['isbn']:
                    my_trade = {
                        'id': trade.id,
                        'book': BookViewModel(trade.book),
                        'count': trade_count['count']
                    }
                    self.trades.append(my_trade)

