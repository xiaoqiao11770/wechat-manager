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
    token='your_token',
    appid='your_appid',
    appsecret='your_appsecret',
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
    )
    return weconf