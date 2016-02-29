#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import PlazaList
from tutorial.items import PlazaItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "plaza_list"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=['http://www.dianping.com/search/category/7/20/g119']




    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)

        total=sel.xpath('//*[@class="page"]/a/@data-ga-page').extract()[-2].strip()
        for i in range(int(total)):
            url='http://www.dianping.com/search/category/7/20/g119p'+str(i+1)
            r = Request(url, callback=self.parse_next)
            req.append(r)

        return req

    def parse_next(self, response):
        req = []
        sel = Selector(response)

        plaza_list=sel.xpath('//*[@data-hippo-type="shop"]')
        for plaza in plaza_list:
            urlend= plaza.xpath('@href').extract()[0].strip()
            url='http://www.dianping.com'+urlend
            r = Request(url, callback=self.parse_detail)
            req.append(r)
        return req

    def parse_detail(self, response):

        sel = Selector(response)
        plazaCity=sel.xpath('//*[@class="city J-city"]/text()').extract()[0].strip()
        plazaName=''
        if sel.xpath('//*[@class="shop-name"]/text()'):
            plazaName=sel.xpath('//*[@class="shop-name"]/text()').extract()[0].strip()
        if sel.xpath('//*[@class="market-name"]/text()'):
            plazaName=sel.xpath('//*[@class="market-name"]/text()').extract()[0].strip()

        isHasShop='否'

        for tmpstr in sel.xpath('//*[@class="item current"]/text()'):
            print tmpstr.extract().strip()
            if tmpstr.extract().strip()=='大家爱逛的店铺':
                isHasShop='是'

        item=PlazaList()
        item['plazaCity']=plazaCity
        item['plazaName']=plazaName
        item['plazaUrl']=response.url.strip()
        item['isHasShop']=isHasShop
        return  item







