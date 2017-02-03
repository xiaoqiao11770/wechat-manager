# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib

import config
from function.messages import receive, reply

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/wx', methods=['GET', 'POST'])
def weixin():
    try:
        if request.method == 'GET':
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
        else:
            print '=' * 20, 'POSE', '=' * 20
            webData = request.stream.read()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
    except Exception, Argument:
        return Argument


def GET():
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


def POST(self):
    try:
        webData = request.stream.read()
        print "Handle Post webdata is ", webData   #后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = "test"
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print "暂且不处理"
            return "success"
    except Exception, Argment:
        return Argment
