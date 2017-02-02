from flask import Flask, request
import hashlib
import xml.etree.ElementTree as ET

import config


app = Flask(__name__)
#config.default_config(app)
#config.wechat_config()


@app.route('/')
def index():
    return "Hello World!"


@app.route('/wx', methods=['GET', 'POST'])
def weixin():
    try:
        data = ''
        if request.method == 'GET':
            data = request.args
            print 'GET', '=' * 20, data
        elif request.method == 'POST':
            rec = request.stream.read()
            xml_rec = ET.fromstring(rec)
            msgtype = xml_rec.find('MsgType').text
            tou = xml_rec.find('ToUserName').text
            fromu = xml_rec.find('FromUserName').text
            content = xml_rec.find('Content').text
            print 'POST', '=' * 20, msgtype, '=' * 20, tou, '=' * 20, fromu, '=' * 20, content
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
    except Exception, Argument:
        return Argument