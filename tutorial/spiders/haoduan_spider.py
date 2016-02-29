#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
from tutorial.items import MobileItem
from scrapy.selector import Selector
import sys

#---------------------------------------------------------------------------
class MobileSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "haoduan"
    #download_delay = 0.3
    start_urls=[]
    f = open("keyword/tel")
    for line in f:
        urltmp="http://61.135.169.121/s?wd="+line.strip()+" 号段"
        start_urls.append(urltmp)


    def parse(self, response):
        '获取商铺详情页'
        sel= Selector(response)
        telinfo=sel.xpath('//*[@class="op_mobilephone_r"]')

        mobile=response.url.replace("%20%E5%8F%B7%E6%AE%B5","").split("wd=")[-1]
        if telinfo:
            item=MobileItem()
            tel=telinfo.xpath('span[2]/text()')
            value=tel.extract()[0].replace(u'\xa0', u' ').strip()
            value_arr=value.split(" ")
            if len(value_arr)==4:
                province=value_arr[0]
                city=value_arr[1]
            else:
                province=value_arr[0]
                city=value_arr[0]
            item['mobile']=mobile
            item['province']=province
            item['city']=city+"市"
            return item










