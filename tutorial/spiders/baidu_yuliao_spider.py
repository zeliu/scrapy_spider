#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import YuLiao
from tutorial.items import PlazaItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
import urllib
import urllib2
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "baidu_yuliao"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/baidukeywords3")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        urltmp="http://61.135.169.121/s?wd="+line.strip()+" 品牌"
        start_urls.append(urltmp)

    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        keyWords=urllib2.unquote(response.url.split('=')[-1]).encode('utf-8')
        urllist=sel.xpath('//*[@id="content_left"]/div/h3/a/@href')

        for i in range(3):
            url=urllist.extract()[i].strip()
            item=YuLiao()
            item['data']=url
            item['keyWords']=keyWords
            req.append(item)

        return req








