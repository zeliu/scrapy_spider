#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import MobileItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "haoma"
    #download_delay = 0.7
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://www.jiahaoma.com/"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        telinfo=sel.xpath('//*[@class="listleft"]/div/div[2]/ul/li/a/@href')

        for tel in telinfo:
            print tel.extract()
            url="http://www.jiahaoma.com"+tel.extract()
            r = Request(url, callback=self.parse_haoduan)
            req.append(r)
        return req



    def parse_haoduan(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        telinfo=sel.xpath('//*[@class="haoduanlist"]/ul/li')

        for tel in telinfo:
            if tel.xpath('div/a'):
                item=MobileItem()
                haoduan=tel.xpath('div[1]/a[1]/text()').extract()[0]
                chengshi=tel.xpath('div[3]/a[1]/text()').extract()[0]
                chengshi_ary=chengshi.split("省")
                province=''
                city=''
                if len(chengshi_ary)==2:
                    province=chengshi_ary[0]
                    city=chengshi_ary[1]
                else:
                    province=chengshi_ary[0]
                    city=chengshi_ary[0]
                item['mobile']=haoduan
                item['province']=province
                item['city']=city
                req.append(item)
        return req



