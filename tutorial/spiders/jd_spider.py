#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import JDItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "jd"
    #download_delay = 0.7
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://dc.3.cn/category/get?callback=getCategoryCallback"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []

        body= response.body.decode('gbk').replace('getCategoryCallback(','')[:-1]
        s = json.loads(body)
        datas=s["data"]
        for data in datas:
            for first_list in data["s"]:
                first=first_list["n"]
                for second_list in first_list["s"]:
                    second=second_list["n"]
                    for third_list in second_list["s"]:
                        third=third_list["n"]
                        if (first.split('|')[1]!='彩票' and first.split('|')[1]!='图书' and first.split('|')[1] !='理财' and second.split('|')[1]!='汽车品牌' and second.split('|')[1]!='汽车车型' and second.split('|')[1]!='京东通信' and third.split('|')[1]!='选号码' and  third.split('|')[1]!='装宽带' and third.split('|')[1]!='中国移动' and third.split('|')[1]!='中国联通' and third.split('|')[1]!='中国电信'):
                            item = JDItem()
                            item['first']=first.split('|')[1]
                            item['second']=second.split('|')[1]
                            item['third']=third.split('|')[1]
                            cat=third.split('|')[0]
                            url='http://list.jd.com/list.html?cat='+cat.replace('-',',')
                            if cat[:4]=='list':
                                url='http://'+cat
                            r = Request(url, callback=self.parse_brand)
                            r.meta['item'] = item
                            print 'url-222------------'+url
                            req.append(r)
        return req

    def parse_brand(self,response):
        req = []
        sel = Selector(response)
        '取品牌'
        brand_list=sel.xpath('//*[@class="J_valueList v-fixed"]/li/a[1]')
        itemtmp = response.meta['item']
        for brands in brand_list:
            brand_name=brands.xpath('text()').extract()[0]
            brand_url=brands.xpath('@href').extract()[0]
            url='http://list.jd.com/'+brand_url
            r = Request(url, callback=self.parse_nextpage)
            item = JDItem()
            item['brandName']=brand_name
            item['first']=itemtmp['first']
            item['second']=itemtmp['second']
            item['third']=itemtmp['third']
            r.meta['item'] = item
            print 'url-3333------------'+url
            req.append(r)
        return req

    def parse_nextpage(self,response):
        req = []
        sel = Selector(response)
        '下一页地址'
        item = response.meta['item']
        url_next=sel.xpath('//*[@class="pn-next"]/@href').extract()#[0]
        total=sel.xpath('//*[@class="fp-text"]/i[1]/text()').extract()[0]
        if url_next:
            for page in range(int(total)):
                url='http://list.jd.com/'+url_next[0].replace('page=2','page='+str(page+1))
                r = Request(url, callback=self.parse_list)
                r.meta['item'] = item
                print 'url-4444------------'+url
                req.append(r)
        return req

    def parse_list(self,response):
        items = []
        req = []
        sel = Selector(response)
        '商品列表页'
        itemtmp = response.meta['item']
        goods_list=sel.xpath('//*[@class="gl-item"]/div[1]')
        name_list=sel.xpath('//*[@class="gl-item"]/div[1]/*[@class="p-name"]')
        url_list=sel.xpath('//*[@class="gl-item"]/div[1]/*[@class="p-img"]')
        sku_list=''
        for i in range(len(goods_list)):
            sku_id=goods_list[i].xpath('@data-sku').extract()[0]
            #listtmp=goods.xpath('div')
            #nametmp=''
            #urltmp=''
            #for li in listtmp:
            #    if li.xpath('@class').extract()[0]=='p-name':
            #        nametmp=li.xpath('a[1]/em[1]/text()').extract()[0]
            #    if li.xpath('@class').extract()[0]=='p-img':
            #        urltmp=li.xpath('a[1]/@href').extract()[0]
            name=name_list[i].xpath('a[1]/em[1]/text()').extract()[0]
            url=url_list[i].xpath('a[1]/@href').extract()[0]
            item = JDItem()
            item['skuId']=sku_id
            if sku_list=='':
                sku_list='J_'+sku_id
            sku_list=sku_list+','+'J_'+sku_id
            item['url']=url
            item['name']=name
            item['first']=itemtmp['first']
            item['second']=itemtmp['second']
            item['third']=itemtmp['third']
            item['brandName']=itemtmp['brandName']
            items.append(item)
        urlnext='http://p.3.cn/prices/mgets?&my=list_price&type=1&skuIds='+sku_list
        r = Request(urlnext, callback=self.parse_price)
        r.meta['items'] = items
        req.append(r)
        return req

    def parse_price(self,response):
        itemstmp = response.meta['items']
        items=[]
        '价格列表'
        price_list=json.loads(response.body)
        for prices in price_list:
            skuid=prices['id']
            price=prices['p']
            delprice=prices['m']
            for item in itemstmp:
                if 'J_'+item['skuId']==skuid:
                    item['price']=price
                    item['delprice']=delprice
                    items.append(item)

        return items



