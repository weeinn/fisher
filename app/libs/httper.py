# -*-coding = utf-8 -*-

# @Time: 2021/3/2 19:51
# @Author: bistro
# @File: httper.py
# @Software: PyCharm
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        res = requests.get(url)
        if res.status_code != 200:
            return {} if return_json else ''
        return res.json() if return_json else res.text