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
    name = "mobile"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/tel")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        urltmp="http://tel.chaxunchina.com/?telnum="+line.strip()
        start_urls.append(urltmp)


    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        telinfo=sel.xpath('//*[@class="telinfo"]/tr')
        print '--------------------------------------'
        mobile=response.url.split("=")[-1]
        for tel in telinfo:
            name=tel.xpath("td/text()").extract()[0].strip()
            if name=='归属地':
                value=tel.xpath("td/text()").extract()[1].strip()
                value_arr=value.split(" ")
                province=''
                city=''
                if len(value_arr)==2:
                    province=value_arr[0]
                    city=value_arr[1]
                else:
                    province=value_arr[0]
                    city=value_arr[0]
                item=MobileItem()

                item['mobile']=mobile
                item['province']=province
                item['city']=city+"市"
                req.append(item)
        return req
