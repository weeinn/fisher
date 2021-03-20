# -*-coding = utf-8 -*-

# @Time: 2021/3/2 19:47
# @Author: bistro
# @File: helper.py
# @Software: PyCharm
def is_isbn_or_key(word):
    isbn_or_key = 'key'
    word = word.strip()
    if len(word) == 13 and word.isdigit():  # 判断13位的ISBN
        isbn_or_key = 'isbn'
    if '-' in word and len(word.replace('-', '')) == 10 and word.isdigit():  # 判断带-的10位ISBN
        isbn_or_key = 'isbn'
    return isbn_or_key
