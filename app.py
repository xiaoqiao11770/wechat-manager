# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib

import config
from function.messages import handle

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/wx', methods=['GET', 'POST'])
def weixin():
    try:
        if request.method == 'GET':
            return get()
        else:
            handle.Handle.POST()

    except Exception, Argument:
        return Argument


def get():
    data = request.args
    print '=' * 20, 'GET', '=' * 20
    print 'DATA===>>', data
    if len(data) == 0:
        return "hello, this is handle view"
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    echostr = data.get('echostr', '')
    token = "test_houdini"

    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    print "handle/GET func: hashcode, signature: ", hashcode, signature
    if hashcode == signature:
        return echostr
    else:
        return ""
