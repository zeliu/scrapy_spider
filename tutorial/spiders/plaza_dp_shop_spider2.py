#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import PlazaShop
from tutorial.items import ShopTag
from tutorial.items import ShopRecommend
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "plaza_dp_shop2"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/plaza")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        arr=line.split('\t')
        wandaPlazaName=arr[0]
        plazaUrl=arr[1]

        start_urls.append(plazaUrl.strip())


    def parse(self, response):
        '获取商铺详情页'
        req = []
        plazaId=response.url.split('/')[-1]
        sel = Selector(response)
        gouwu=sel.xpath('//*[@class="hot-top fn-clear"]/div')
        i=1
        for gouwushop in gouwu:
            shopsurl='http://www.dianping.com'+gouwushop.xpath('a[1]/@href').extract()[0].strip()
            shopImg=[]
            shopImg=gouwushop.xpath('a[1]/img/@src').extract()
            item=PlazaShop()
            item['plazaId']=plazaId
            if i<=4:
                item['shopCatetory1']='购物'
            else:
                item['shopCatetory1']='餐饮'
            item['shopUrl']=shopsurl
            item['image_urls']=shopImg
            r = Request(shopsurl, callback=self.shop_detail)
            r.meta['item'] = item
            i=i+1
            req.append(r)

        return req



    def shop_detail(self, response):

        req=[]
        sel = Selector(response)
        'shop详情页'
        shopId=response.url.split('/')[-1]
        shopName=sel.xpath('//*[@class="shop-name"]/text()').extract()[0].strip()
        address1=''
        address2=''
        if sel.xpath('//*[@class="expand-info address"]/a[1]/span[1]/text()'):
            address1=sel.xpath('//*[@class="expand-info address"]/a[1]/span[1]/text()').extract()[0].strip()
        if sel.xpath('//*[@class="expand-info address"]/span[2]/text()'):
            address2=sel.xpath('//*[@class="expand-info address"]/span[2]/text()').extract()[0].strip()
        addr=address1+address2
        floorRule=re.compile(r"(.*?)(\w{1,4})(层|楼)")
        floor=''
        room=''
        addrlist=[]
        if '楼' in addr:
            addrlist=addr.split('楼')
        if '层' in addr:
            addrlist=addr.split('层')
        if len(addrlist)>=2:
            room=addrlist[-1]

        floortmp=floorRule.match(addr.encode('UTF-8'))
        if floortmp:
            floor=floortmp.group(2)+'层'
        shopTel=''
        #shopStar=''
        #shopComment=''
        #shopAvg=''
        #shopScore1=''
        #shopScore2=''
        #shopScore3=''
        shopTime=''
        shopTags=''
        if sel.xpath('//*[@itemprop="tel"]/text()').extract():
            shopTel=sel.xpath('//*[@itemprop="tel"]/text()').extract()[0].strip()
        itemtmp = response.meta['item']

        otherList=sel.xpath('//*[@class="other J-other Hide"]/p')

        for other in otherList:
            str=''
            if other.xpath('span[1]/text()').extract():
                str= other.xpath('span[1]/text()').extract()[0].strip()
            if '营业时间' in str:
                shopTime=other.xpath('span[2]/text()').extract()[0].strip()
            if '分类标签' in str:
                tag_list=other.xpath('span')
                for tag in tag_list:
                    if tag.xpath('@class').extract()[0].strip()!='info-name':
                        tagitem=ShopTag()
                        if tag.xpath('a[1]/text()'):
                            tagName=tag.xpath('a[1]/text()').extract()[0].strip()
                            shopTags=shopTags+'|'+tagName

        shop=PlazaShop()
        shop['plazaId']=itemtmp['plazaId']
        shop['shopId']=shopId
        shop['shopName']=shopName.replace('\n','').replace('\r','')
        shop['shopTel']=shopTel.replace('\n','').replace('\r','')

        shop['shopAddress']=addr.replace('\n','').replace('\r','')
        shop['shopFloor']=floor
        shop['shopRoom']=room
        shop['shopCatetory1']=itemtmp['shopCatetory1']

        shop['image_urls']=itemtmp['image_urls']
        shop['shopTime']=shopTime.replace('\n','').replace('\r','')
        shop['shopTag']=shopTags[1:].replace('\n','').replace('\r','')

        return shop


