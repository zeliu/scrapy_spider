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
    name = "kankan"
    allowed_domains = ["kankan.com"]

    start_urls = [
        "http://movie.kankan.com/type,order/teleplay,hits/"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        sel = Selector(response)
        total=sel.xpath('//*[@class="list-pager-v2"]/a/text()').extract()[-2]
        for i in range(int(total)):
            url='http://movie.kankan.com/type,order/teleplay,hits/'
            if i!=0:
                url='http://movie.kankan.com/type,order/teleplay,hits/page'+str(i+1)+'/'
            r = Request(url, callback=self.parse_list)
            req.append(r)
        return req


    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '电影列表'
        movie_list = sel.xpath('//*[@class="movielist"]/li/p[1]')
        count_list=sel.xpath('//*[@class="update"]')
        for i in range(len(movie_list)):
            item =TeleplayItem()
            item['name'] = movie_list[i].xpath('a/@title').extract()[0]
            if movie_list[i].xpath('em/text()').extract():
                item['episode'] = movie_list[i].xpath('em/text()').extract()[0]
            url=movie_list[i].xpath('a/@href').extract()[0]
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
        directer_list=[]
        if sel.xpath('//*[@class="movieinfo"]/li[2]/a/text()').extract():
            directer_list=sel.xpath('//*[@class="movieinfo"]/li[2]/a/text()').extract()
        directer=''
        for directertmp in directer_list:
            directer=directer+'/'+directertmp.strip()

        actor_list=[]
        if sel.xpath('//*[@class="movieinfo"]/li[3]/a/text()').extract():
            actor_list=sel.xpath('//*[@class="movieinfo"]/li[3]/a/text()').extract()
        actor=''
        for actortmp in actor_list:
            actor=actor+'/'+actortmp.strip()
        year =''
        if sel.xpath('//*[@class="movieinfo_tt"]/h2[1]/span[1]/text()'):
            year=sel.xpath('//*[@class="movieinfo_tt"]/h2[1]/span[1]/text()').extract()[0]

        type_list=[]
        if sel.xpath('//*[@class="movieinfo"]/li[5]/a/text()').extract():
            type_list=sel.xpath('//*[@class="movieinfo"]/li[5]/a/text()').extract()
        type=''
        for typetmp in type_list:
            type=type+'/'+typetmp.strip()
        area=''
        if sel.xpath('//*[@class="movieinfo"]/li[4]/a/text()').extract():
            area=sel.xpath('//*[@class="movieinfo"]/li[4]/a/text()').extract()[0]
        #socre_shi='0'
        #socre_ge='.0'
        #if sel.xpath('//*[@id="total_shi"]/text()').extract():
        #    socre_shi=sel.xpath('//*[@id="total_shi"]/text()').extract()[0]
        #if sel.xpath('//*[@id="total_ge"]/text()').extract():
        #    socre_ge=sel.xpath('//*[@id="total_ge"]/text()').extract()[0]

        #score=  socre_shi+socre_ge
        #commentCnts=''
        #if sel.xpath('//*[@id="pj_all_num"]/text()').extract():
        #    commentCnts=sel.xpath('//*[@id="pj_all_num"]/text()').extract()[0]

        playCnts=''
        if sel.xpath('//*[@class="widemode"]/script[1]/text()').extract():
            playCnts=sel.xpath('//*[@class="widemode"]/script[1]/text()').extract()[0].replace('var G_PLAY_VV = { total:"','').replace('" }','')
        item['name'] = itemtmp['name']
        item['episode'] = itemtmp['episode']
        item['area'] = area
        item['directer']=directer[1:].strip()
        item['type']=type[1:].strip()
        item['actor']=actor[1:].strip()
        item['playCnts']=playCnts
        item['id']=response.url.split('/')[-1].split('.')[0]
        #item['score']=score
        #item['commentCnts']=commentCnts
        #item['id'] = itemtmp['id']
        item['year']=year
        urlt=response.url.split('/')[-2]
        url='http://app11.kankan.com/movie_rating/data/'+urlt+'/'+str(response.url.split('/')[-1].split('.')[0])+'.js'
        r = Request(url, callback=self.parse_js)
        r.meta['item'] = item
        return r


    def parse_js(self, response):
        s=json.loads(response.body.replace('var xunlei_movie_data=','').replace(';',''))
        item=response.meta['item']
        item['score']=s['rating']
        item['commentCnts']=s['rating_people_num']
        return item




