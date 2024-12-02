#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python

from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()