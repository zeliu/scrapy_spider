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
    name = "plaza_dp_shop"
    download_delay = 0.5
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/plaza")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        arr=line.split('\t')
        wandaPlazaName=arr[0]
        plazaUrl=arr[1]
        print '@@@@@@@@@@:'+wandaPlazaName
        print '$$$$$$4444:'+plazaUrl
        start_urls.append(plazaUrl.strip())


    def parse(self, response):
        '获取商铺详情页'
        req = []
        plazaId=response.url.split('/')[-1]
        sel = Selector(response)
        tmplist=['10']
        plazaShop_list=sel.xpath('//*[@class="mod-title"]/a')
        for plazaShops in plazaShop_list:
            str=plazaShops.xpath('text()').extract()[0]
            if str=='更多店铺':
                for category in tmplist:
                    if category=='10':
                        shopsurl='http://www.dianping.com'+plazaShops.xpath('@href').extract()[0].replace('20_','10_').strip()
                        shopCatetory1='餐饮'
                    if category=='20':
                        shopsurl='http://www.dianping.com'+plazaShops.xpath('@href').extract()[0].replace('20_','20_').strip()
                        shopCatetory1='购物'
                    shopStreet=plazaShops.xpath('@href').extract()[0].split('/')[-2].replace('20_','').strip()
                    item=PlazaShop()
                    item['plazaId']=plazaId
                    item['shopStreet']=shopStreet
                    item['shopCatetory1']=shopCatetory1
                    item['shopUrl']=shopsurl
                    r = Request(shopsurl, callback=self.shop_next_page)
                    r.meta['item'] = item
                    req.append(r)

        return req


    def shop_next_page(self, response):

        req=[]
        sel = Selector(response)
        '下一页地址'
        total=1
        print '222222222222222222:'+str(len(sel.xpath('//*[@class="page"]/a/text()').extract()))
        if len(sel.xpath('//*[@class="page"]/a/text()').extract())>=2:

            total=sel.xpath('//*[@class="page"]/a/text()').extract()[-2]
        item = response.meta['item']
        if total>5:
            total=5
        for page in range(int(total)):
            url=item['shopUrl']+'p'+str(page+1)
            r = Request(url, callback=self.shop_list)
            r.meta['item'] = item
            print 'url-4444------------'+url
            req.append(r)
        return req

    def shop_list(self, response):

        req=[]
        sel = Selector(response)
        'shop列表'
        shopList=sel.xpath('//*[@class="shop-list J_shop-list shop-all-list"]/ul[1]/li')
        itemtmp = response.meta['item']
        for shop in shopList:
            url='http://www.dianping.com'+shop.xpath('div[1]/a[1]/@href').extract()[0]
            img=[]
            imgtmp=shop.xpath('div[1]/a[1]/img/@data-src').extract()[0]
            if 'http' not in imgtmp:
                #imgtmp='http:'+imgtmp
                continue

            img.append(imgtmp)
            #url=shop.xpath('//div[@class="pic"]/a[1]/@href').extract()[0]
            addr=shop.xpath('div[2]/div[3]/span[1]/text()').extract()[0]
            shopType=shop.xpath('div[2]/div[3]/a[1]/span[1]/text()').extract()[0].strip()
            if itemtmp['shopStreet'] in addr:
                if (itemtmp['shopCatetory1']=='购物' and shopType=='服饰鞋包') or (itemtmp['shopCatetory1']=='餐饮'):
                    r = Request(url, callback=self.shop_detail)
                    shop=PlazaShop()
                    shop['shopAddress']=addr
                    floorRule=re.compile(r"(.*?)(\w{1,4})(层|楼)")
                    #roomRule=re.compile(r"(.*?)(层|楼)(.*?)(\w{1,40})")
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
                    #roomtmp=roomRule.match(addr.encode('UTF-8'))
                    #if roomtmp:
                    #    room=roomtmp.group(4)
                    shop['shopFloor']=floor
                    shop['shopRoom']=room
                    shop['shopCatetory1']=itemtmp['shopCatetory1']
                    shop['plazaId']=itemtmp['plazaId']
                    shop['image_urls']=img
                    r.meta['item'] = shop
                    req.append(r)
        return req

    def shop_detail(self, response):

        req=[]
        sel = Selector(response)
        'shop详情页'
        shopId=response.url.split('/')[-1]
        shopName=sel.xpath('//*[@class="shop-name"]/text()').extract()[0].strip()
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
        briefList=sel.xpath('//*[@class="brief-info"]/span')
        itemtmp = response.meta['item']
        #for brief in briefList:
        #    if brief.xpath('text()').extract():
        #        text=brief.xpath('text()').extract()[0].strip()
        #        if text=='':
        #            shopStar=brief.xpath('@class').extract()[0].strip()
        #        if '评论' in text:
        #            shopComment=text.replace('条','').replace('评论','')
        #        if '人均' in text:
        #            shopAvg=text.replace('人均：','').replace('元','')
        #        if '口味' in text:
        #            shopScore1=text.replace('口味：','').replace('元','')
        #        if '环境' in text:
        #            shopScore2=text.replace('环境：','').replace('元','')
        #        if '服务' in text:
        #            shopScore3=text.replace('服务：','').replace('元','')
        #    else:
        #        shopStar=brief.xpath('@class').extract()[0].replace('mid-rank-stars mid-str','').strip()
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
                        #if tag.xpath('text()[2]'):
                        #    tagitem['tagScore']=tag.xpath('text()[2]').extract()[0].replace('(','').replace(')','').strip()
                        #shopTags.append(tagitem)
        #recommend_list=sel.xpath('//*[@class="recommend-name"]/a')
        #shopRecommends=[]
        #for recommends in recommend_list:
        #    shopRec=ShopRecommend()
        #    shopRec['recName']=recommends.xpath('text()').extract()[0].strip()
        #    shopRec['recScore']=recommends.xpath('em[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #    shopRecommends.append(shopRec)
        shop=PlazaShop()
        shop['plazaId']=itemtmp['plazaId']
        shop['shopId']=shopId
        shop['shopName']=shopName.replace('\n','').replace('\r','')
        shop['shopTel']=shopTel.replace('\n','').replace('\r','')
        #shop['shopStar']=shopStar
        #shop['shopAvg']=shopAvg
        #shop['shopScore1']=shopScore1
        #shop['shopScore2']=shopScore2
        #shop['shopScore3']=shopScore3
        #shop['shopComment']=shopComment
        shop['shopAddress']=itemtmp['shopAddress'].replace('\n','').replace('\r','')
        shop['shopFloor']=itemtmp['shopFloor'].replace('\n','').replace('\r','')
        shop['shopRoom']=itemtmp['shopRoom'].replace('\n','').replace('\r','')
        shop['shopCatetory1']=itemtmp['shopCatetory1']

        shop['image_urls']=itemtmp['image_urls']
        shop['shopTime']=shopTime.replace('\n','').replace('\r','')
        shop['shopTag']=shopTags[1:].replace('\n','').replace('\r','')
        #shop['shopRecommend']=shopRecommends

        return shop


