#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import BaiduTranslate
from scrapy import Request
import datetime
from scrapy.selector import Selector
import sys
from urllib import urlencode
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "baidu_translate"
    start_urls = [
        "http://www.baidu.com"
    ]

    def parse(self, response):
        '获取商铺详情页'
        req = []
        url='http://fanyi.baidu.com/v2transapi'
        f = open("keyword/baidutranslate")
        for line in f:
            item =BaiduTranslate()
            item['zh']=line.strip()
            mybody='from=zh&to=en&query='+line.strip()
            r = Request(url,method='POST',body=mybody,callback=self.parse_translate,headers={"Content-Type":"application/x-www-form-urlencoded"})
            r.meta['item'] = item
            print r.body
            req.append(r)
        return req
    def parse_translate(self, response):
        req = []
        itemtmp = response.meta['item']
        s=json.loads(response.body)
        item=BaiduTranslate()
        item['zh']=itemtmp['zh']
        en= s['trans_result']['data'][0]['dst']
        item['en']=en

        return item
