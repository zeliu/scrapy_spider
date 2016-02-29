#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "db"
    allowed_domains = ["douban.com"]

    start_urls = [
        "http://www.douban.com/tag/2012/movie"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        '下一页地址'
        next_list = sel.xpath('//*[@class="next"]')

        url =  next_list.xpath('a[1]/@href').extract()[0]
        print '--------nexturl----------'+url
        r = Request('http://www.douban.com/tag/2012/movie'+str(url), callback=self.parse)
        r.headers.setdefault('User-Agent', ua)
        req.append(r)

        '商铺详情页'
        movie_list = sel.xpath('//*[@class="mod movie-list"]/dl/dd')
        for movie in movie_list:
                url=movie.xpath('a[1]/@href').extract()[0]
                #price=shop.xpath('div[1]/em[1]/text()').extract()[0]
                #addr=shop.xpath('div[2]/text()').extract()[0]
                #print 'price:'+str(price)
                #print 'addr:'+str(addr)
                print '------url:---------'+str(url)
                r = Request(url, callback=self.parse_comments)
                r.headers.setdefault('User-Agent', ua)
                req.append(r)
        return req



    def parse_comments(self,response):

        '获取评价信息'
        sel = Selector(response)
        #items = []
        score=sel.xpath('//*[@class="ll rating_num"]/text()').extract()[0]
        counts=sel.xpath('//*[@class="rating_wrap clearbox"]/p[2]/a[1]/span[1]/text()').extract()[0]
        moviename=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        movieid=sel.xpath('/html/head/link[4]/@href').extract()[0].split('/')[-2]
        item = TutorialItem()
        item['score'] = score
        item['counts'] = counts
        item['moviename'] = moviename.strip()
        item['movieid'] = movieid.strip()
        #items.append(item)
        return item
        ############################################################################