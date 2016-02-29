#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import urllib
from tutorial.items import JukuuTranslate
from scrapy import Request
import re
import sys
import json
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "yicool"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]

    start_urls=[]
    f = open("keyword/translate_zh")
    for line in f:
        urltmp="http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx?word="+line.strip()
        start_urls.append(urltmp)



    def parse(self, response):
        '获取商铺详情页'
        req = []
        body= response.body
        s = json.loads(body)

        pagecount=s['pagecount']
        print '**************:'+str(pagecount)
        if pagecount!=0:
            keyword=response.url.split("word=")[-1]
            item=JukuuTranslate()
            item['keyword']=urllib.unquote(keyword)
            for page in range(int(pagecount)):
                url="http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx?word="+keyword+"&page="+str(page+1)
                r = Request(url,callback=self.parse_translate)
                r.meta['item'] = item
                req.append(r)
        return req


    def parse_translate(self, response):
        '获取商铺详情页'
        req=[]
        s = json.loads(response.body)
        itemtmp = response.meta['item']
        translate_list=s['sentence']
        dr = re.compile(r'<[^>]+>',re.S)
        for sentence in translate_list:
            item=JukuuTranslate()
            item['keyword']=itemtmp['keyword']
            ru=dr.sub('',sentence['ru'])
            item['ru']=ru
            item['zh']=dr.sub('',sentence['chs'])
            #print dr.sub('',sentence['ru'])
            #print dr.sub('',sentence['chs'])
            req.append(item)
        return req







