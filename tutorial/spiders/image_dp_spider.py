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
    name = "image_dp"
    download_delay = 3
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%8C%97%E4%BA%AC+%E9%87%91%E5%9C%B0%E4%B8%AD%E5%BF%83+&oq=%E5%8C%97%E4%BA%AC+%E9%87%91%E5%9C%B0%E4%B8%AD%E5%BF%83+&rsp=-1"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        #print response.body
        imagelist=sel.xpath('//*[@class="imglist clearfix pageNum0"]/li')
        script_list=sel.xpath('/html/script')
        print str(len(script_list))
        print script_list.extract()[-1]
        for images in imagelist:
            imagehref=images.xpath('div[1]/a[1]/@href').extract()[0].strip()
            print imagehref

        return req








