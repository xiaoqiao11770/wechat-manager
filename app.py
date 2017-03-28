# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib

# import config
# import function.tuling as tuling
# from function.messages import receive, reply
# from function.nodes import read

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply

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
            # if hashcode == signature:
            #     return echostr
            # else:
            #     return ""
            try:
                check_signature(token, signature, timestamp, nonce)
            except InvalidSignatureException:
                print 'Authentication failed'
                return ''
        else:
            print '=' * 20, 'POSE', '=' * 20
            webData = request.stream.read()
            print "Handle Post webdata is ", webData   #后台打日志
            # recMsg = receive.parse_xml(webData)
            msg = parse_message(webData)
            # if isinstance(recMsg, receive.Msg):
            #     toUser = recMsg.FromUserName
            #     print "to User ====>", toUser
            #     fromUser = recMsg.ToUserName
            #     print "from User ====>", fromUser
            #     if recMsg.MsgType == 'text':
            #         rec_content = recMsg.Content
            #         content = read.type_nodes(rec_content)
            #         if not content:
            #             try:
            #                 node_type, node_name = read.find_node(rec_content)
            #                 node_hand = read.Read(node_type, node_name).hand()
            #                 node_bewirte = read.Read(node_type, node_name).bewirte()
            #                 content = node_hand + "\n" + "-------" + "\n" + node_bewirte
            #             except:
            #                 content = tuling.result(rec_content)
            #             content = content.encode('utf-8')
            #         replyMsg = reply.TextMsg(toUser, fromUser, content)
            #         return replyMsg.send()
            #     if recMsg.MsgType == 'image':
            #         mediaId = recMsg.MediaId
            #         replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
            #         return replyMsg.send()
            #
            #     else:
            #         return reply.Msg().send()
            reply = TextReply(message=msg)
            reply.content = 'text reply'
            # 转换成 XML
            xml = reply.render()
            return xml
            # else:
            #     print "暂且不处理"
            #     return "success"
    except Exception, Argument:
        return Argument
