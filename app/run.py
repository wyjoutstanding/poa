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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)