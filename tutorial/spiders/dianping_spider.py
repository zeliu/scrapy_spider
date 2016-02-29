#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import DPItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "dianping"
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
            url='http://www.dianping.com'+urltmp
            r = Request(url, callback=self.parse_detail)
            r.meta['item'] = itemtmp
            req.append(r)
        return req

    def parse_detail(self, response):
        sel = Selector(response)
        item=response.meta['item']
        url=response.url
        shopName=sel.xpath('//*[@class="shop-name"]/text()').extract()[0].strip()
        star=''
        commentCnts=''
        avgPrice=''
        tasteScore=''
        surrScore=''
        serviceScore=''
        for basic in sel.xpath('//*[@class="brief-info"]/span'):
            if basic.xpath('@title').extract():
                if '星' in basic.xpath('@title').extract()[0]:
                    star=basic.xpath('@title').extract()[0]
            if basic.xpath('text()').extract():
                if '评论' in basic.xpath('text()').extract()[0]:
                    commentCnts=basic.xpath('text()').extract()[0]
                if '均' in basic.xpath('text()').extract()[0]:
                    avgPrice=basic.xpath('text()').extract()[0]
                if '味' in basic.xpath('text()').extract()[0]:
                    tasteScore=basic.xpath('text()').extract()[0]
                if '环境' in basic.xpath('text()').extract()[0]:
                    surrScore=basic.xpath('text()').extract()[0]
                if '服务' in basic.xpath('text()').extract()[0]:
                    serviceScore=basic.xpath('text()').extract()[0]
        adr1=''
        adr2=''
        address=''
        if len(sel.xpath('//*[@itemprop="street-address"]/@title').extract())>=2:
            adr2=sel.xpath('//*[@itemprop="street-address"]/@title').extract()[1]
        if len(sel.xpath('//*[@itemprop="street-address"]/@title').extract())==1:
            adr2=sel.xpath('//*[@itemprop="street-address"]/@title').extract()[0]
        if sel.xpath('//*[@itemprop="locality region"]/text()').extract():
            adr1=sel.xpath('//*[@itemprop="locality region"]/text()').extract()[0]

        address=adr1+adr2
        phone=sel.xpath('//*[@class="expand-info tel"]/span')
        tel=''
        for i in range(len(phone)):
            if i !=0:
                tel=tel+phone[i].xpath('text()').extract()[0]+','
        time=''
        if  sel.xpath('//*[@class="other J-other"]/p[1]/span[2]/text()').extract():
            time=sel.xpath('//*[@class="other J-other"]/p[1]/span[2]/text()').extract()[0]
        serive=''
        if len(sel.xpath('//*[@class="info J-feature"]/a[1]/text()').extract())>=2:
            serive=sel.xpath('//*[@class="info J-feature"]/a[1]/text()').extract()[1]
        tag_list=sel.xpath('//*[@class="info info-indent"]/span')
        tag=' '
        for tagtmp in tag_list:
            if tagtmp.xpath('a[1]'):
                txt=tagtmp.xpath('a[1]/text()').extract()[0].strip()
                cnts=tagtmp.xpath('text()').extract()[0].strip()
                tag=tag+txt+cnts+','
        dish_list=sel.xpath('//*[@class="recommend-name"]/a')
        dish=''
        for dishtmp in dish_list:
            dishname=dishtmp.xpath('@title').extract()[0]
            dishcnts=dishtmp.xpath('em/text()')
            dish=dishname+dishcnts
        item['shopName']=shopName.strip()
        item['star']=star.strip()
        item['commentCnts']=commentCnts.strip()
        item['avgPrice']=avgPrice.strip()
        item['tasteScore']=tasteScore.strip()
        item['surrScore']=surrScore.strip()
        item['serviceScore']=serviceScore.strip()
        item['address']=address.strip()
        item['tel']=tel[:-1].strip()
        item['time']=time.strip()
        item['tag']=tag[:-1].strip()
        item['service']=serive.strip()
        item['dish']=dish.strip()
        item['url']=url

        return item







