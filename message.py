from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError


class MessageManager(object):
    def __init__(self, conf, signature='', timestamp='', nonce=''):
        self.wechat = WechatBasic(conf=conf)
        # check wechat connect.
        if self.wechat.check_signature(signature, timestamp, nonce):
            print 'Accept'
        else:
            print 'Wrong'

    def receive(self, body_text):
        try:
            self.wechat.parse_data(body_text)
        except ParseError:
            print 'Invalid Body Text'
        id = self.wechat.message.id  # 对应于 XML 中的 MsgId
        target = self.wechat.message.target  # 对应于 XML 中的 ToUserName
        source = self.wechat.message.source  # 对应于 XML 中的 FromUserName
        time = self.wechat.message.time  # 对应于 XML 中的 CreateTime
        type = self.wechat.message.type  # 对应于 XML 中的 MsgType
        raw = self.wechat.message.raw  # 原始 XML 文本，方便进行其他分析
        if isinstance(self.wechat.message, TextMessage):
            content = self.wechat.message.content   # 对应于 XML 中的 Content


        if isinstance(self.wechat.message, ImageMessage):
            picurl = self.wechat.message.picurl  # 对应于 XML 中的 PicUrl
            media_id = self.wechat.message.media_id  # 对应于 XML 中的 MediaId


        if isinstance(self.wechat.message, VoiceMessage):
            media_id = self.wechat.message.media_id  # 对应于 XML 中的 MediaId
            format = self.wechat.message.format  # 对应于 XML 中的 Format
            recognition = self.wechat.message.recognition  # 对应于 XML 中的 Recognition


        if isinstance(self.wechat.message, VideoMessage) or isinstance(self.wechat.message, ShortVideoMessage):
            media_id = self.wechat.message.media_id  # 对应于 XML 中的 MediaId
            thumb_media_id = self.wechat.message.thumb_media_id  # 对应于 XML 中的 ThumbMediaId


        if isinstance(self.wechat.message, LocationMessage):
            location = self.wechat.message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
            scale = self.wechat.message.scale  # 对应于 XML 中的 Scale
            label = self.wechat.message.label  # 对应于 XML 中的 Label


        if isinstance(self.wechat.message, LinkMessage):
            title = self.wechat.message.title  # 对应于 XML 中的 Title
            description = self.wechat.message.description  # 对应于 XML 中的 Description
            url = self.wechat.message.url  # 对应于 XML 中的 Url

        if isinstance(self.wechat.message, EventMessage):
            if self.wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                key = self.wechat.message.key  # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
                ticket = self.wechat.message.ticket  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
            elif self.wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
                pass
            elif self.wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
                key = self.wechat.message.key  # 对应于 XML 中的 EventKey
                ticket = self.wechat.message.ticket  # 对应于 XML 中的 Ticket
            elif self.wechat.message.type == 'location':  # 上报地理位置事件
                latitude = self.wechat.message.latitude  # 对应于 XML 中的 Latitude
                longitude = self.wechat.message.longitude  # 对应于 XML 中的 Longitude
                precision = self.wechat.message.precision  # 对应于 XML 中的 Precision
            elif self.wechat.message.type == 'click':  # 自定义菜单点击事件
                key = self.wechat.message.key  # 对应于 XML 中的 EventKey
            elif self.wechat.message.type == 'view':  # 自定义菜单跳转链接事件
                key = self.wechat.message.key  # 对应于 XML 中的 EventKey
            elif self.wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
                status = self.wechat.message.status  # 对应于 XML 中的 Status
            elif self.wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                         'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
                key = self.wechat.message.key  # 对应于 XML 中的 EventKey

    def reply(self, type='text'):
        if type == 'text':
            # xml = self.wechat.response_text(content='文本回复')
            xml = self.wechat.response_text(content='文本回复', escape=True)
        if type == 'image':
            xml = self.wechat.response_image(media_id='media_id')
        if type == 'voice':
            xml = self.wechat.response_voice(media_id='media_id')
        if type == 'video':
            xml = self.wechat.response_video(media_id='media_id', title='video_title', description='video_description')
        if type == 'music':
            xml = self.wechat.response_music(
                music_url='your_music_url',
                title='music_title',
                description='music_description',
                hq_music_url='your_hq_music_url',
                thumb_media_id='your_thumb_media_id',
            )
        if type == 'news':
            xml = self.wechat.response_news([
                {
                    'title': u'第一条新闻标题',
                    'description': u'第一条新闻描述，这条新闻没有预览图',
                    'url': u'http://www.google.com.hk/',
                }, {
                    'title': u'第二条新闻标题, 这条新闻无描述',
                    'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': u'http://www.github.com/',
                }, {
                    'title': u'第三条新闻标题',
                    'description': u'第三条新闻描述',
                    'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': u'http://www.v2ex.com/',
                }
            ])
