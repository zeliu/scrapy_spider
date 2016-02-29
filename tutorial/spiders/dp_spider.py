#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    handle_httpstatus_list = [403]
    name = "dp"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://wap.dianping.com/shoplist/1"
    ]

    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        print str(response.body)
        '下一页地址'
        next_list = sel.xpath('//*[@class="pagelink"]')
        print 'ad:'+str(next_list[0].xpath('text()').extract()[0].encode('utf-8'))
        for page in next_list:
            if page.xpath('text()').extract()[0].encode('utf-8')=='下一页':
                url =  page.xpath('@href').extract()[0]
                print '--------afag----------'+url
                r = Request(url, callback=self.parse)
                req.append(r)

        '商铺详情页'
        shop_list = sel.xpath('//*[@class="shop-list"]/ul[1]/li')
        for shop in shop_list:
                storeid=shop.xpath('a[1]/@href').extract()[0].split('/')[-1]
                #price=shop.xpath('div[1]/em[1]/text()').extract()[0]
                #addr=shop.xpath('div[2]/text()').extract()[0]
                #print 'price:'+str(price)
                #print 'addr:'+str(addr)
                url='http://www.dianping.com/shop/'+str(storeid)+'/review_all'
                print '------nexturl:---------'+str(url)
                r = Request(url, callback=self.next_page)
                req.append(r)
        return req


    def next_page(self,response):
        req = []
        sel = Selector(response)
        '下一页地址'
        next_list = sel.xpath('//*[@class="PageLink"]')
        total=int(next_list[-1].xpath('@title').extract()[0])
        shopid=sel.xpath('//*[@class="revitew-title"]/h1[1]/a[1]/@href').extract()[0].split('/')[-1]
        #print '-----dafaa:---'+str(total)
        for page in range(total):
            url =  'http://www.dianping.com/shop/'+str(shopid)+'/review_all?pageno='+str(page)#+str(page.xpath('@href').extract()[0])
            print '--------afag2:----------'+url
            r = Request(url, callback=self.parse_comments)
            req.append(r)
        return req

    def parse_comments(self,response):

        '获取评价信息'
        sel = Selector(response)
        items = []
        shopid=sel.xpath('//*[@class="revitew-title"]/h1[1]/a[1]/@href').extract()
        shopname=sel.xpath('//*[@class="revitew-title"]/h1[1]/a[1]/@title').extract()
        userid=sel.xpath('//*[@class="pic"]/a[1]/@user-id').extract()
        name=sel.xpath('//*[@class="pic"]/p[1]/a[1]/text()').extract()
        score=sel.xpath('//*[@class="user-info"]/span/@title').extract()
        comment=sel.xpath('//*[@class="J_brief-cont"]/text()').extract()
        brand_name=sel.xpath('//*[@class="misc-name"]/text()').extract()
        time=sel.xpath('//*[@class="time"]/text()').extract()
        for i in range(len(userid)):
            item = TutorialItem()
            item['store_id'] = shopid[0].split('/')[-1].strip()
            item['store_name'] = shopname[0].strip()
            item['name'] = name[i].strip()
            #item['brand_name'] = brand_name[i].strip()
            item['score'] = score[i].strip()
            item['userid'] = userid[i].strip()
            item['time'] = time[i].strip()
            item['comment'] = comment[i].strip().replace('\n','').replace('\r','')
            items.append(item)
        #item = response.meta['item']

        return items
        ############################################################################