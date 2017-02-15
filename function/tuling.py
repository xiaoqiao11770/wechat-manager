# -*- coding: utf-8 -*-
import urllib,urllib2
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

API_KEY = 'a0109075bd174e7e879d0c3a1df30ec1'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY

def result(query):
    for i in range(1,100):
        TULINURL = "%s%s" % (raw_TULINURL,urllib2.quote(query))
        req = urllib2.Request(url=TULINURL)
        result = urllib2.urlopen(req).read()
        hjson=json.loads(result)
        #length=len(hjson.keys())
        content=hjson['text']
        return content.decode('utf-8')

if __name__=='__main__':
    print result('哈哈哈')