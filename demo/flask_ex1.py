# -*- coding: utf-8 -*-

from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_word():
    return 'hello world!'

@app.route('/login/', methods=['POST'])
def login():
    print("hello")
    username = request.form.get('username')
    password = request.form.get('password')
    # print(username, password)
    return username+password

if __name__ == "__main__":
    app.run(debug=True)