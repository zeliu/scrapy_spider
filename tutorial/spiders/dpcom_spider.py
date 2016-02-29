#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
from tutorial.items import DPItem
from tutorial.items import CommentsItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "dpcom"
    #download_delay = 0.7
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://www.dianping.com/beijing"
    ]
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        my_list = sel.xpath('//*[@class="secondary-category J-secondary-category"]')
        print str(len(my_list))
        for my in my_list:
            if my.xpath('a[1]/text()').extract():
                first= my.xpath('a[1]/text()').extract()[0]
                if first=='美食频道':
                    second_list=my.xpath('a')
                    for i in range(len(second_list)):
                        if i!=0:
                            second= second_list[i].xpath('text()').extract()[0]
                            url='http://www.dianping.com'+second_list[i].xpath('@href').extract()[0]
                            item=DPItem()
                            item['first']=first
                            item['second']=second
                            r = Request(url, callback=self.parse_third)
                            r.meta['item'] = item
                            req.append(r)

        return req

    def parse_third(self, response):
        req =[]
        sel = Selector(response)
        itemtmp=response.meta['item']
        my_list = sel.xpath('//*[@class="nc-items nc-sub"]/a')
        for i in range(len(my_list)):
            if i !=0:
                third=my_list[i].xpath('span/text()').extract()[0]
                item=DPItem()
                item['first']=itemtmp['first']
                item['second']=itemtmp['second']
                item['third']=third
                url='http://www.dianping.com'+my_list[i].xpath('@href').extract()[0]
                item['url']=url
                r = Request(url, callback=self.parse_nextpage)
                r.meta['item'] = item
                req.append(r)

        return req

    def parse_nextpage(self, response):
        req =[]
        sel = Selector(response)
        itemtmp=response.meta['item']
        page='1'
        if len(sel.xpath('//*[@class="page"]/a/text()').extract())>=2:
            page = sel.xpath('//*[@class="page"]/a/text()').extract()[-2]
        print '----1212121----------'+str(page)
        for i in range(int(page)):
            url=itemtmp['url']+'p'+str(i+1)
            print '-----------url:----------'+url
            r = Request(url, callback=self.parse_link)
            r.meta['item'] = itemtmp
            req.append(r)

        return req

    def parse_link(self, response):
        req =[]
        sel = Selector(response)
        itemtmp=response.meta['item']
        link_list=sel.xpath('//*[@class="shop-list J_shop-list shop-all-list"]/ul[1]/li/div[1]')
        for link in link_list:
            urltmp=link.xpath('a[1]/@href').extract()[0]
            url='http://www.dianping.com'+urltmp+'/review_more'
            print '888888888888888url88888'+url
            r = Request(url, callback=self.parse_commentpage)
            r.meta['item'] = itemtmp
            req.append(r)
        return req

    def parse_commentpage(self, response):
        req=[]
        sel = Selector(response)
        urltmp=response.url
        itemtmp=response.meta
        total='1'
        if sel.xpath('//*[@class="PageLink"]/@title').extract():
            total=sel.xpath('//*[@class="PageLink"]/@title').extract()[-1]
        for i in range(int(total)):
            url=urltmp+'?pageno='+str(i+1)
            r = Request(url, callback=self.parse_comments)
            r.meta['item'] = itemtmp
            req.append(r)

        return req

    def parse_comments(self, response):
        items=[]
        sel = Selector(response)
        shopId=sel.xpath('//*[@class="info-name"]/h2[1]/a[1]/@href').extract()[0].split('/')[-1]
        shopName=sel.xpath('//*[@class="info-name"]/h2[1]/a[1]/text()').extract()[0]
        shopStar=sel.xpath('//*[@class="info-name"]/div[1]/span[1]/@title').extract()[0]
        shopAvg=sel.xpath('//*[@class="stress"]/text()').extract()[0]
        name_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="name"]/a[1]/text()').extract()
        contribution_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="contribution"]/span[1]/@title').extract()
        score_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="content"]/div[1]')
        rts_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="comment-rst"]')
        comments_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="J_brief-cont"]/text()').extract()
        time_list=sel.xpath('//*[@class="comment-list"]/ul/li//*[@class="time"]/text()').extract()
        for i in range(len(name_list)):
            item=CommentsItem()
            item['username']=name_list[i].strip()
            item['contribution']=contribution_list[i].strip()
            span_list=score_list[i].xpath('span')
            if span_list:
                if span_list[0].xpath('@titile'):
                    item['star']=span_list[0].xpath('@titile').extract()[0]
                if len(span_list)==2:
                    item['avg']=span_list[1].xpath('text()').extract()[0]
            item['serviceScore']=rts_list[i].xpath('span[3]/text()').extract()[0]
            item['tasteScore']=rts_list[i].xpath('span[1]/text()').extract()[0]
            item['surrScore']=rts_list[i].xpath('span[2]/text()').extract()[0]
            item['comments']=comments_list[i].strip()
            item['time']=time_list[i].strip()
            item['shopId']=str(shopId).strip()
            item['shopName']=shopName.strip()
            item['shopStar']=shopStar.strip()
            item['shopAvg']=shopAvg.strip()
            items.append(item)
        return items





