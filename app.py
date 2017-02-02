from flask import Flask, request
import tornado.web

import hashlib
import xml.etree.ElementTree as ET

import config
from function import message
from wechat_sdk import WechatConf, WechatBasic

app = Flask(__name__)

#config.default_config(app)
we_config = config.wechat_config()
conf = WechatConf(
    token=we_config['token'],
    appid=we_config['appid'],
    appsecret=we_config['appsecret'],
    encrypt_mode=we_config['encrypt_mode'],
    encoding_aes_key=['encoding_aes_key']
)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/wx', methods=['GET', 'POST'])
def weixin():
    try:
        if request.method == 'GET':
            get()
        elif request.method == 'POST':
            post()

    except Exception, Argument:
        return Argument


def post():
    rec = request.stream.read()
    xml_rec = ET.fromstring(rec)
    msgtype = xml_rec.find('MsgType').text
    tou = xml_rec.find('ToUserName').text
    fromu = xml_rec.find('FromUserName').text
    content = xml_rec.find('Content').text
    print 'POST', '=' * 20, msgtype, '=' * 20, tou, '=' * 20, fromu, '=' * 20, content
    print '===rec===*' * 20, rec, '===xml_rec===' * 20, xml_rec

    wechat = WechatBasic(conf=conf)
    body = tornado.web.RequestHandler.request.body
    print 'body====>>>', body
    message.MessageManager(conf=conf).receive(body)
    message.MessageManager(conf=conf).reply()


def get():
    data = request.args
    print 'GET', '=' * 20, data
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