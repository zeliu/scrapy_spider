#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import urllib
from tutorial.items import JukuuTranslate
from scrapy import Request
from scrapy.selector import Selector
import sys
import re
import math
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "iciba"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]

    #start_urls=[]
    #f = open("keyword/translate_zh")
    #for line in f:
    #    urltmp="http://dj.iciba.com/"+line.strip()+"-1.html"
    #    start_urls.append(urltmp)

    start_urls=["http://dj.iciba.com/聊天"]


    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        keyword=response.url.split("/")[-1]
        item=JukuuTranslate()
        item['keyword']=urllib.unquote(keyword)

        if sel.xpath('//*[@class="stc_list"]/script/text()'):
            pagetmp=int(sel.xpath('//*[@class="stc_list"]/script/text()').extract()[0].strip().replace('dj_count = ','').replace(';',''))
            total=int(math.floor(pagetmp/10))+1
            for page in range(total):
                url="http://dj.iciba.com/"+keyword+"-1-"+str(page+1)+"-%01-0-0.html"
                r = Request(url,callback=self.parse_translate)
                r.meta['item'] = item
                req.append(r)
        return req

    def parse_translate(self, response):
        '获取商铺详情页'
        req=[]
        sel = Selector(response)
        itemtmp = response.meta['item']
        translate_list=sel.xpath('/html/body/li')
        for translate in translate_list:
            item=JukuuTranslate()
            item['keyword']=itemtmp['keyword']
            english=translate.xpath('p[1]/span[2]/@con').extract()[0].replace('"','').strip()
            item['en']=english
            chinese=translate.xpath('p[2]/span[2]/@con').extract()[0].replace('"','').strip()
            item['zh']=chinese
            req.append(item)
        return req







