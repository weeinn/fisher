# -*-coding = utf-8 -*-

# @Time: 2021/3/3 10:36
# @Author: bistro
# @File: __init__.py
# @Software: PyCharm

# models实体层不需要在init文件进行导入加载，因为如果和模型有关，
# 那么相关文件都会进行导入然后在使用，避免了循环导入的这样一种情况
from app.models import book
from app.models import drift
