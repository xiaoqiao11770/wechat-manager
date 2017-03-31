# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

from function.read_node import read
from function import tuling

# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', 'test_houdini')
AES_KEY = os.getenv('WECHAT_AES_KEY', 'XUi5VjeFWb7v5LFVIFOwL0iT0fQLTQv3TkLrZfigu6h')
APPID = os.getenv('WECHAT_APPID', 'wx332e0321845c6e3c')

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        print('echo_str:', echo_str)
        return echo_str
    print '============ successful validation ============'
    print('signature:', signature)
    print('timestamp: ', timestamp)
    print('nonce:', nonce)
    print('encrypt_type:', encrypt_type)
    print('msg_signature:', msg_signature)

    # POST request
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(request.data)
        print 'Msg Type: ', msg.type
        if msg.type == 'text':
            print '============ text mag ============'
            user_content = msg.content
            print('user_content:', user_content)
            node_data = read.parse_node(user_content)
            if node_data:
                run_content = node_data[0] + '\n' + node_data[2]
                articles = [
                    {
                        'title': user_content.upper(),
                        'description': node_data[0],
                        'image': 'http://www.sidefx.com/docs/houdini/icons/SOP/%s.svg' % user_content,
                        'url': node_data[2]
                    },
                    # add more ...
                ]
                reple = create_reply(articles, msg)
                return reple.render()
            else:
                run_content = tuling.result(user_content.encode("utf-8"))
            print('run_content:', run_content)
            reply = create_reply(run_content, msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        return reply.render()

    elif encrypt_type == 'subscribe':
        print '===> The is subscribe'
        msg = parse_message(request.data)
        content = '欢迎关注特效Houdini，这里有个聊天机器人，你可以调戏她。'
        reply = create_reply(content, message=msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply('Sorry, can not handle this for now', msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
