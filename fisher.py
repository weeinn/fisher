# -*-coding = utf-8 -*-

# @Time: 2020/12/10 20:58
# @Author: 小酒馆
# @File: basic.py
# @Software: PyCharm

from app import create_app
app = create_app()

if __name__ == "__main__":  # 生产环境nginx+uwsgi
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81, threaded=True)  # 允许外网访问设置host=0.0.0.0
