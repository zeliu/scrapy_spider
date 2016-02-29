#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class JdSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "test"
    store_name = ""
    store_id = ""
    allowed_domains = ["meituan.com"]
    start_urls = [
        "http://bj.meituan.com/category/meishi"
    ]

    def parse(self, response):
        '获取商铺详情页'
        req = []

        '下一页地址'
        next_list = response.xpath('//*[@class="next"]/a/@href').extract()

        if next_list:
            url = 'http://bj.meituan.com'+next_list[0]
            r = Request(url, callback=self.parse)
            req.append(r)

        '商铺详情页'
        for sel in response.xpath('//*[@class="poi-tile__head"]'):
            for url in sel.xpath('@href').extract():
                if 'shop' in url:
                    r = Request(url, callback=self.parse_nextpage)
                    req.append(r)
        return req
    def parse_nextpage(self, response):
        '获取商铺详情页'
        req = []

        urltmp=response.xpath('/html/head/link[10]/@href').extract()
        shopid = urltmp[0].split('/')[-1]
        #print('----------'+str(shopid))
        self.store_name=response.xpath('//*[@class="fs-section__left"]/h2[1]/span[1]/text()').extract()
        self.store_id=shopid
        urltmp2=response.xpath('//*[@class="paginator-wrapper"]/div[1]/@data-total').extract()
        totaldata = int(urltmp2[0])
        #print('----------'+str(totaldata))
        for data in range(totaldata):
            if data%10==0:
                #print data
                url = 'http://bj.meituan.com/deal/feedbacklist/0/'+shopid+'/all/0/default/1?limit=10&showpoititle=0&offset='+str(data)
                r = Request(url, callback=self.parse_comments)
                req.append(r)
        return req

    def parse_comments(self,response):


        '获取评价信息'
        #print('-----ss------'+str(response.body))
        #s = json.loads(response.body)
        #print(s["data"]["ratelistHtml"])
        #store_name=response.xpath('//*[@class="fs-section__left"]/h2[1]/span[1]/text()').extract()
        #names = response.xpath('//*[@class="J-rate-list"]/li/div[1]/p/span[1]/text()').extract()
        #level = response.xpath('//*[@class="J-rate-list"]/li/div[1]/p/span[2]/i/@title').extract()
        #score = response.xpath('//*[@class="review-content-wrapper"]/div[1]/div[1]/span[1]/span[1]/@style').extract()
        #time = response.xpath('//*[@class="review-content-wrapper"]/div[1]/span[1]/text()').extract()
        #comment = response.xpath('//*[@class="review-content-wrapper"]/div[2]/p/text()').extract()
        s = json.loads(response.body)
        #print(s["data"]["ratelistHtml"])
        sel = s["data"]["ratelistHtml"]
        ids=Selector(text=sel).xpath('//*[@class="J-ratelist-item rate-list__item cf"]/@data-rateid').extract()
        names=Selector(text=sel).xpath('//*[@class="J-ratelist-item rate-list__item cf"]/div[1]/p[1]/span[1]/text()').extract()
        levels=Selector(text=sel).xpath('//*[@class="J-ratelist-item rate-list__item cf"]/div[1]/p[1]/span[2]/i/@title').extract()
        scores=Selector(text=sel).xpath('//*[@class="rate-stars"]/@style').extract()

        times=Selector(text=sel).xpath('//*[@class="review-content-wrapper"]/div[1]/span[1]/text()').extract()
        comments = Selector(text=sel).xpath('//*[@class="review-content-wrapper"]/div[2]/p/text()').extract()


        items = []

        for i in range(len(ids)):
            item = TutorialItem()
            item['id'] = ids[i].strip()
            item['store_id'] = self.store_id.strip()
            item['store_name'] = self.store_name[0].strip()
            item['name'] = names[i].strip()
            item['level'] = levels[i].strip()
            item['score'] = scores[i].strip()
            item['time'] = times[i].strip()
            item['comment'] = comments[i].strip().replace('\n','').replace('\r','')
            items.append(item)
        #item = response.meta['item']

        return items
        ############################################################################