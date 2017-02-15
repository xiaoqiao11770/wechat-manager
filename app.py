# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib

import config
import function.tuling as tuling
from function.messages import receive, reply
from function.nodes import read

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
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                print "to User ====>", toUser
                fromUser = recMsg.ToUserName
                print "from User ====>", fromUser
                if recMsg.MsgType == 'text':
                    rec_content = recMsg.Content
                    node_list = read.Read('sop', rec_content).node_list()
                    if rec_content in node_list:
                        node_read = read.Read('sop', rec_content)
                        content = node_read.hand() + '\r\n' + node_read.bewirte()
                    else:
                        content = function.tuling.result(rec_content)
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()

                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                return "success"
    except Exception, Argument:
        return Argument
