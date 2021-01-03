# -*- coding: utf-8 -*-

from flask import Flask, session
# pip install flask-cors
from flask_cors import CORS

app = Flask(__name__)
# 跨域处理
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

import config

app.config['SECRET_KEY'] = config.SECRET_KEY

from auth import auth
from api import public_api

app.register_blueprint(auth.auth_bp)
app.register_blueprint(public_api.api_bp)

import global_init

if __name__ == "__main__":
    config._init() # 全局数据配置
    global_init.global_data_init()
    app.run(host='0.0.0.0', debug=True)
