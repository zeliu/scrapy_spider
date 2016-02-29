#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import WeatherItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
#---------------------------------------------------------------------------
class TianqiSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "tianqitmp"
    #download_delay = 0.7
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid=0"
    ]


    def parse(self, response):
        '获取商铺详情页'
        req = []

        body= response.body.decode('gbk').replace('getZoneInfo(','')[:-1]
        s = json.loads(body)
        datas=s[0]
        item=WeatherItem()
        item['provinceId']=10
        item['province']='山西'
        url='http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid='+str(10)
        r = Request(url, callback=self.parse_city)
        r.meta['item'] = item
        req.append(r)
        return req

    def parse_city(self, response):
        '获取商铺详情页'
        req = []
        itemtmp = response.meta['item']
        body= response.body.decode('gbk').replace('getZoneInfo(','')[:-1]
        s = json.loads(body)
        datas=s[0]

        item=WeatherItem()
        item['provinceId']=itemtmp['provinceId']
        item['province']=itemtmp['province']
        item['cityId']=1001
        item['city']='太原'
        url='http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid='+str(1001)
        r = Request(url, callback=self.parse_county)
        r.meta['item'] = item
        print 'url-333------------'+url
        req.append(r)
        return req

    def parse_county(self, response):
        '获取商铺详情页'
        req = []
        items=[]
        itemtmp = response.meta['item']
        body= response.body.decode('gbk').replace('getZoneInfo(','')[:-1]
        s = json.loads(body)
        datas=s[0]

        item=WeatherItem()
        item['provinceId']=itemtmp['provinceId']
        item['province']=itemtmp['province']
        item['cityId']=itemtmp['cityId']
        item['city']=itemtmp['city']
        item['countyId']=101100101
        item['county']='太原'
        url='http://lishi.tianqi.com/'+str(datas['py'][101100101])+'/index.html'
        r = Request(url, callback=self.parse_weather)
        r.meta['item'] = item
        print 'url-333------------'+url
        req.append(r)
        #items.append(item)
        return req

    def parse_weather(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        itemtmp = response.meta['item']
        url_list=sel.xpath('//*[@class="tqtongji1"]/ul/li/a/@href').extract()#[0]
        for url in url_list:
            monthtmp=url.split('/')[-1].split('.')[0]
            #if monthtmp>='201507':
            item=WeatherItem()
            item['provinceId']=itemtmp['provinceId']
            item['province']=itemtmp['province']
            item['cityId']=itemtmp['cityId']
            item['city']=itemtmp['city']
            item['countyId']=itemtmp['countyId']
            item['county']=itemtmp['county']
            item['month']=monthtmp
            r = Request(url, callback=self.parse_detail)
            r.meta['item'] = item
            print 'url-333------------'+url
            req.append(r)
        return req
    def parse_detail(self, response):
        '获取商铺详情页'
        items=[]
        sel = Selector(response)
        itemtmp = response.meta['item']
        weather_list=sel.xpath('//*[@class="tqtongji2"]/ul')
        for i in range(len(weather_list)):
            if i!=0:
                day=''
                if weather_list[i].xpath('li[1]/text()').extract():
                    day=weather_list[i].xpath('li[1]/text()').extract()[0]
                if weather_list[i].xpath('li[1]/a[1]/text()').extract():
                    day=weather_list[i].xpath('li[1]/a[1]/text()').extract()[0]
                max=''
                if weather_list[i].xpath('li[2]/text()').extract():
                    max=weather_list[i].xpath('li[2]/text()').extract()[0]
                min=''
                if weather_list[i].xpath('li[3]/text()'):
                    min=weather_list[i].xpath('li[3]/text()').extract()[0]
                weather=''
                if weather_list[i].xpath('li[4]/text()').extract():
                    weather=weather_list[i].xpath('li[4]/text()').extract()[0]
                windD=''
                if weather_list[i].xpath('li[5]/text()').extract():
                    windD=weather_list[i].xpath('li[5]/text()').extract()[0]
                windP=''
                if weather_list[i].xpath('li[6]/text()').extract():
                    windP=weather_list[i].xpath('li[6]/text()').extract()[0]
                item=WeatherItem()
                item['provinceId']=itemtmp['provinceId']
                item['province']=itemtmp['province']
                item['cityId']=itemtmp['cityId']
                item['city']=itemtmp['city']
                item['countyId']=itemtmp['countyId']
                item['county']=itemtmp['county']
                item['month']=itemtmp['month']
                item['day']=day
                item['max']=max
                item['min']=min
                item['weather']=weather
                item['windD']=windD
                item['windP']=windP
                items.append(item)

        return items

