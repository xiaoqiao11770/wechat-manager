# -*- coding: utf-8 -*-
import os.path


def default_config(app):
    conf_data = dict(
    DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    DEBUG = True,
    SECRET_KEY = 'development key',
    USERNAME= 'admin',
    PASSWORD= 'default',
    )
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    return conf_data


def wechat_config():
    weconf = dict(
    token='test_houdini',
    appid='wx332e0321845c6e3c',
    appsecret='e2bb9f5d4af14943d8c0121d61cf50ed',
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='XUi5VjeFWb7v5LFVIFOwL0iT0fQLTQv3TkLrZfigu6h'  # 如果传入此值则必须保证同时传入 token, appid
    )
    return weconf