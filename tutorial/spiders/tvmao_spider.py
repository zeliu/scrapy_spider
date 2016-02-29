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
    name = "tvmao"
    allowed_domains = ["tvmao.com"]

    start_urls = [
        "http://www.tvmao.com/tv_genre.jsp?type=drama&category=0&satellite=true&alltime=false"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        sel = Selector(response)
        total=sel.xpath('//*[@class="sum"]/text()').extract()[0].replace('共','').replace('页','')
        for i in range(int(total)):
            url='http://www.tvmao.com/tv_genre.jsp?type=drama&category=0&satellite=true&alltime=false'
            if i!=0:
                url='http://www.tvmao.com/tv_genre.jsp?type=drama&category=0&satellite=true&alltime=false&start='+str(i*20)
            r = Request(url, callback=self.parse_list)
            req.append(r)
        return req


    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '电影列表'
        movie_list = sel.xpath('//*[@class="cateobjsr"]/div[1]/a[1]')
        for i in range(len(movie_list)):
            item =TeleplayItem()
            item['name'] = movie_list[i].xpath('text()').extract()[0]
            url= 'http://www.tvmao.com'+movie_list[i].xpath('@href').extract()[0]
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
        if sel.xpath('//*[@itemprop="numberOfEpisodes"]/text()'):
            episode=sel.xpath('//*[@itemprop="numberOfEpisodes"]/text()').extract()[0]


        directer_list=[]
        if sel.xpath('//*[@itemprop="director"]/text()').extract():
            directer_list=sel.xpath('//*[@itemprop="director"]/text()').extract()
        directer=''
        for directertmp in directer_list:
            directer=directer+'/'+directertmp.strip()

        actor_list=[]
        if sel.xpath('//*[@itemprop="actors"]/text()').extract():
            actor_list=sel.xpath('//*[@itemprop="actors"]/text()').extract()
        actor=''
        for actortmp in actor_list:
            actor=actor+'/'+actortmp.strip()
        year =''
        if sel.xpath('//*[@itemprop="datePublished"]/text()'):
            year=sel.xpath('//*[@itemprop="datePublished"]/text()').extract()[0]

        type_list=[]
        if sel.xpath('//*[@itemprop="genre"]/text()').extract():
            type_list=sel.xpath('//*[@itemprop="genre"]/text()').extract()
        type=''
        for typetmp in type_list:
            type=type+'/'+typetmp.strip()
        area=''
        if sel.xpath('//*[@itemprop="contentLocation"]/text()').extract():
            area=sel.xpath('//*[@itemprop="contentLocation"]/text()').extract()[0]

        language=''
        if sel.xpath('///*[@itemprop="inLanguage"]/text()').extract():
            language=sel.xpath('//*[@itemprop="inLanguage"]/text()').extract()[0]
        socre_shi='0'
        socre_ge='.0'
        if sel.xpath('//*[@class="unit"]/text()').extract():
            socre_shi=sel.xpath('//*[@class="unit"]/text()').extract()[0]
        if sel.xpath('//*[@class="decimal"]/text()').extract():
            socre_ge=sel.xpath('//*[@class="decimal"]/text()').extract()[0]

        score=  socre_shi+socre_ge
        commentCnts=''
        if sel.xpath('//*[@itemprop="reviews"]/text()').extract():
            commentCnts=sel.xpath('//*[@itemprop="reviews"]/text()').extract()[0]


        guanzhuCnts=''
        if sel.xpath('//*[@itemprop="interactionCount"]/text()').extract():
            guanzhuCnts=sel.xpath('//*[@itemprop="interactionCount"]/text()').extract()[0]
        scoreCnts=''
        if sel.xpath('//*[@class="mt5 clear"]/a[3]/span[1]/text()').extract():
            scoreCnts=sel.xpath('//*[@class="mt5 clear"]/a[3]/span[1]/text()').extract()[0]
        item['name'] = itemtmp['name']
        item['area'] = area
        item['directer']=directer[1:].strip()
        item['type']=type[1:].strip()
        item['actor']=actor[1:].strip()
        item['guanzhuCnts']=guanzhuCnts
        item['scoreCnts']=scoreCnts
        item['score']=score
        item['commentCnts']=commentCnts
        item['year']=year
        item['episode']=episode
        item['language']=language
        return item




