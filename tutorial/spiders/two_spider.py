#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import TeleplayItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "two"
    allowed_domains = ["2345.com"]

    start_urls = [
        "http://tv.2345.com/---.html"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        sel = Selector(response)
        total=sel.xpath('//*[@id="pageList"]/a/text()').extract()[-4]
        for i in range(int(total)):
            url='http://tv.2345.com/---.html'
            if i!=0:
                url='http://tv.2345.com/----default-'+str(i+1)+'.html'
            r = Request(url, callback=self.parse_list)
            req.append(r)
        return req


    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '电影列表'
        movie_list = sel.xpath('//*[@data-ajax83="ys_tv_list_title"]')
        for i in range(len(movie_list)):
            item =TeleplayItem()
            item['name'] = movie_list[i].xpath('@title').extract()[0]
            url= movie_list[i].xpath('@href').extract()[0]
            r = Request(url, callback=self.parse_detail)
            r.meta['item'] = item
            req.append(r)
        return req


    def parse_detail(self,response):

        '电影详情'
        sel = Selector(response)
        #items = []
        item = TeleplayItem()
        itemtmp=response.meta['item']
        episode=''
        if sel.xpath('//*[@class="tit clearfix"]/p[1]/span[2]/em[1]/text()'):
            episode=sel.xpath('//*[@class="tit clearfix"]/p[1]/span[2]/em[1]/text()').extract()[0]


        directer_list=[]
        if sel.xpath('//*[@class="listCon"]/dl[1]/dd[2]/a/text()').extract():
            directer_list=sel.xpath('//*[@class="listCon"]/dl[1]/dd[2]/a/text()').extract()
        directer=''
        for directertmp in directer_list:
            directer=directer+'/'+directertmp.strip()

        actor_list=[]
        if sel.xpath('//*[@class="dlTxt clearfix"]/dd[1]/a/text()').extract():
            actor_list=sel.xpath('//*[@class="dlTxt clearfix"]/dd[1]/a/text()').extract()
        actor=''
        for actortmp in actor_list:
            actor=actor+'/'+actortmp.strip()
        year =''
        if sel.xpath('//*[@class="listCon"]/dl[2]/dd[2]/a/text()'):
            year=sel.xpath('//*[@class="listCon"]/dl[2]/dd[2]/a/text()').extract()[0]

        type_list=[]
        if sel.xpath('//*[@class="listCon"]/dl[2]/dd[1]/a/text()').extract():
            type_list=sel.xpath('//*[@class="listCon"]/dl[2]/dd[1]/a/text()').extract()
        type=''
        for typetmp in type_list:
            type=type+'/'+typetmp.strip()
        area=''
        if sel.xpath('//*[@class="listCon"]/dl[2]/dd[3]/a/text()').extract():
            area=sel.xpath('//*[@class="listCon"]/dl[2]/dd[3]/a/text()').extract()[0]
        socre=''
        if sel.xpath('//*[@class="tit clearfix"]/p[1]/span[1]/em[1]/text()').extract():
            socre=sel.xpath('//*[@class="tit clearfix"]/p[1]/span[1]/em[1]/text()').extract()[0]

        commentCnts=''
        if sel.xpath('//*[@id="quickComment1"]/em[1]/text()').extract():
            commentCnts=sel.xpath('//*[@id="quickComment1"]/em[1]/text()').extract()[0]



        item['name'] = itemtmp['name']
        item['area'] = area
        item['directer']=directer[1:].strip()
        item['type']=type[1:].strip()
        item['actor']=actor[1:].strip()
        item['commentCnts']=commentCnts
        item['year']=year
        item['episode']=episode
        item['score']=socre
        return item




