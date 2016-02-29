#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import PlazaRecommend
from tutorial.items import PlazaItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "plaza_dp_brand"
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

        sel = Selector(response)
        plazaId=response.url.split('/')[-1]
        brandlist=sel.xpath('//*[@class="mod-body fn-clear"]/div')
        for brands in brandlist:
            pic=''
            brandname=''
            brandpic=[]
            if brands.xpath('div[1]/img/@_src'):
                pic=brands.xpath('div[1]/img/@_src').extract()[0].strip()
                brandpic.append(pic)
            if brands.xpath('div[2]/p[1]/text()'):
                brandname=brands.xpath('div[2]/p[1]/text()').extract()[0].strip()
            item=PlazaItem()
            item['plazaId']=plazaId
            item['brandName']=brandname
            #item['brandPic']=pic
            item['image_urls']=brandpic
            req.append(item)



        #item['image_urls']=plazaImage
        return req









