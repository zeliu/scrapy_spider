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
    name = "letv"
    allowed_domains = ["letv.com"]

    start_urls = [
        "http://list.letv.com/listn/c2_t-1_a-1_y-1_s1_md_o20_d1_p6.html"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        for i in range(34):
            url='http://list.letv.com/apin/chandata.json?c=2&d=1&md=&o=20&p='+str(i+1)+'&s=1'
            r = Request(url, callback=self.parse_list)
            req.append(r)
        return req


    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '电影列表'
        s=json.loads(response.body)
        movie_list = s['album_list']
        for movie in movie_list:
            item =TeleplayItem()
            item['name'] = movie['name']
            item['episode'] = movie['episodes']
            item['area'] = movie['areaName']
            item['language'] = movie['language']
            item['directer']=movie['language']
            item['type']=movie['subCategoryName']
            item['playCnts']=movie['playCount']
            item['id'] = movie['aid']
            url='http://www.letv.com/tv/'+str(movie['aid'])+'.html'
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
        if sel.xpath('//*[@data-statectn="n_textInfo"]/p[1]/a/text()').extract():
            directer_list=sel.xpath('//*[@data-statectn="n_textInfo"]/p[1]/a/text()').extract()
        directer=''
        for directertmp in directer_list:
            directer=directer+'/'+directertmp.strip()

        actor_list=[]
        if sel.xpath('//*[@data-statectn="n_textInfo"]/p[2]/a/text()').extract():
            actor_list=sel.xpath('//*[@data-statectn="n_textInfo"]/p[2]/a/text()').extract()
        actor=''
        for actortmp in actor_list:
            actor=actor+'/'+actortmp.strip()

        year=sel.xpath('//*[@data-statectn="n_textInfo"]/p[4]/a[1]/text()').extract()[0]


        item['name'] = itemtmp['name']
        item['episode'] = itemtmp['episode']
        item['area'] = itemtmp['area']
        item['language'] = itemtmp['language']
        item['directer']=directer[1:].strip()
        item['type']=itemtmp['type']
        item['actor']=actor[1:].strip()
        item['playCnts']=itemtmp['playCnts']
        item['id'] = itemtmp['id']
        item['year']=year
        return item




