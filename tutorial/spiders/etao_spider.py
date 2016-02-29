#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "etao"
    allowed_domains = ["etao.com"]
    start_urls = [
        "http://www.etao.com/haohuo/index.html"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        items = []
        #category_list = sel.xpath('//*[@class="category-list"]')
        #or category in category_list:
        layer_list=sel.xpath('//*[@class="category-layer"]')
        print '-------agag2-----:'+str(len(layer_list))

        for j in range(len(layer_list)):
            first=layer_list[j].xpath('h3[1]/span[1]/text()').extract()[0]
            #second_list=layer_list[j].xpath('//*[@class="sub-category-second"]')
            second_list=layer_list[j].xpath('dl[1]/dt')
            #third_list=layer_list[j].xpath('//*[@class="sub-category-third"]')
            third_list=layer_list[j].xpath('dl[1]/dd')
            print '-------agag-----:'+str(len(second_list))
            for i in range(len(second_list)):
                if second_list[i].xpath('a[1]/text()').extract():
                    second=second_list[i].xpath('a[1]/text()').extract()[0]
                    thirds=third_list[i].xpath('a')
                    for tmp in thirds:
                        third=tmp.xpath('text()').extract()[0]
                        thirdid=tmp.xpath('@href').extract()[0].split('&')[-1]#.split('=')[-1]
                        item = TutorialItem()
                        item['first']=first
                        item['second']=second
                        item['third']=third
                        item['itemthirdid']=thirdid#.split('=')[-1]
                        #items.append(item)
                        url='http://www.etao.com/haohuo/api/ajax.html?s=0&from=filter&v=2.0&mdList=item_more&sort=default&cat&tag&showtxt&'+str(thirdid)
                        r = Request(url, callback=self.parse_nextpage)
                        r.meta['item'] = item
                        print 'url-222------------'+url
                        req.append(r)
        return req

    def parse_nextpage(self,response):
        req = []
        #print(response.body)
        '下一页地址'
        s = json.loads(response.body)
        print '------agageww3e:'+str(s["data"]["total"])
        total=int(s["data"]["total"])
        item = response.meta['item']
        for page in range(total):
            if page%20==0:
                print '---page=------------'+str(page)
                url='http://www.etao.com/haohuo/api/ajax.html?s='+str(page)+'&from=filter&v=2.0&mdList=item_more&sort=default&cat&tag&showtxt&'+str(item['itemthirdid'])
                r = Request(url, callback=self.parse_comments)
                r.meta['item'] = item
                print 'url-3333------------'+url
                req.append(r)
        return req

    def parse_comments(self,response):

        '获取评价信息'
        items = []

        itemtmp = response.meta['item']
        s = json.loads(response.body)
        goods=s['data']['items']
        #print 'len1:'+str(response.body)
        #print 'len:'+str(goods)
        for good in goods:
            item = TutorialItem()
            item['title']=good['title']
            item['price']=good['price']
            item['hpid']=good['hpid']
            item['first']=itemtmp['first']
            item['second']=itemtmp['second']
            item['third']=itemtmp['third']
            item['itemthirdid']=itemtmp['itemthirdid'].split('=')[-1]
            items.append(item)
        return items



