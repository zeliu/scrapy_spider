#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import datetime
from tutorial.items import WeatherItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "tianqiincre"
    download_delay = 1
    #allowed_domains = ["3.cn"]
    start_urls = [
        "http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid=0"
    ]

    month = str(datetime.date.today()).replace('-','')[:-2]
    year = str(datetime.date.today()).replace('-','')[:-4]
    def parse(self, response):
        '获取商铺详情页'
        req = []

        body= response.body.decode('gbk').replace('getZoneInfo(','')[:-1]
        s = json.loads(body)
        datas=s[0]
        for (k,v) in datas['value'].items():
            print "key:"+k+",value:"+str(v)[2:]
            item=WeatherItem()
            item['provinceId']=k
            item['province']=str(v)[2:]
            url='http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid='+str(k)
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
        for (k,v) in datas['value'].items():
            print "key:"+k+",value:"+str(v)[2:]
            item=WeatherItem()
            item['provinceId']=itemtmp['provinceId']
            item['province']=itemtmp['province']
            item['cityId']=k
            item['cityEng']=str(datas['py'][k])
            item['city']=str(v)[2:]
            url='http://www.tianqi.com/weather.php?a=getZoneInfo&type=1&pid='+str(k)
            r = Request(url, callback=self.parse_county)
            r.meta['item'] = item
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
        for (k,v) in datas['value'].items():
            print "key:"+k+",value:"+str(v)[2:]
            item=WeatherItem()
            item['provinceId']=itemtmp['provinceId']
            item['province']=itemtmp['province']
            item['cityId']=itemtmp['cityId']
            item['city']=itemtmp['city']
            item['countyId']=k
            item['county']=str(v)[2:]
            item['month']=self.month
            url='http://'+itemtmp['cityEng']+'.tianqi.com/'+str(datas['py'][k])+'/7/'
            r = Request(url, callback=self.parse_detail)
            r.meta['item'] = item
            req.append(r)
            #items.append(item)
        return req


    def parse_detail(self, response):
        '获取商铺详情页'
        items=[]
        sel = Selector(response)
        itemtmp = response.meta['item']
        weather_list=sel.xpath('//*[@class="today_databg"]/div/div/ul')
        for lis in weather_list:


            day=''
            max=''
            min=''
            weather=''
            windD=''
            windP=''

            for li in lis.xpath('li'):
                liClass=''
                liStyle=''
                if li.xpath('@class'):
                    liClass=li.xpath('@class').extract()[0].strip()
                if li.xpath('@style'):
                    liStyle=li.xpath('@style').extract()[0].strip()
                print '&&&&&&&&&&'+liClass
                if liClass=='time':
                    day=li.xpath('text()').extract()[0].strip()
                if liClass=='fon14 fB':
                    max=li.xpath('span[1]/font[1]/text()').extract()[0].strip()
                    min=li.xpath('span[1]/font[2]/text()').extract()[0].strip()
                if liClass=='cDRed':


                    weather=li.xpath('text()').extract()[0].strip()
                    print '%%%%%%%%%%%%%%%%%%%%'+weather+'%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                if liStyle=='height:18px;overflow:hidden':
                    wind=''
                    windD=''
                    windP=''
                    if li.xpath('text()'):
                        wind=li.xpath('text()').extract()[0].strip()
                    if len(wind.split(' '))>=2:
                        windD=wind.split(' ')[0]
                        windP=wind.split(' ')[1]
                    if wind=='无持续风向微风':
                        windD='无持续风向'
                        windP='微风'
            item=WeatherItem()
            item['provinceId']=itemtmp['provinceId']
            item['province']=itemtmp['province']
            item['cityId']=itemtmp['cityId']
            item['city']=itemtmp['city']
            item['countyId']=itemtmp['countyId']
            item['county']=itemtmp['county']
            item['month']=itemtmp['month']
            item['day']=self.year+'-'+day.replace('（周一）','').replace('（周二）','').replace('（周三）','').replace('（周四）','').replace('（周五）','').replace('（周六）','').replace('（周日）','').replace('月','-').replace('日','').strip()
            item['max']=max
            item['min']=min
            item['weather']=weather
            item['windD']=windD
            item['windP']=windP
            items.append(item)
        weather_list2=sel.xpath('//*[@class="everytqshow"]/div')
        #today = str(datetime.date.today()).replace('-','')
        #today=datetime.date.today()
        #i=0
        #j=3
        for weather2 in weather_list2:
            weatherClass=weather2.xpath('@class').extract()[0].strip()
            day=''
            max=''
            min=''
            weather=''
            windD=''
            windP=''
        #    if weatherClass=='tqshow1':
        #        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        #        day=str(today + datetime.timedelta(i)).replace('-','')
        #        i=i+1
        #        if weather2.xpath('ul[1]/li[2]/font[1]'):
        #            max=weather2.xpath('ul[1]/li[2]/font[1]/text()').extract()[0].strip()
        #        if weather2.xpath('ul[1]/li[2]/font[2]'):
        #            min=weather2.xpath('ul[1]/li[2]/font[2]/text()').extract()[0].strip()
        #        if weather2.xpath('ul[1]/li[3]'):
        #            weather=weather2.xpath('ul[1]/li[3]/text()').extract()[0].strip()
        #        if weather2.xpath('ul[1]/li[4]'):
        #            wind=''
        #            windD=''
        #            windP=''
        #            if li.xpath('text()'):
        #                wind=weather2.xpath('ul[1]/li[4]/text()').extract()[0].strip()
        #            if len(wind.split(' '))>=2:
        #                windD=wind.split(' ')[0]
        #                windP=wind.split(' ')[1]
        #            if wind=='无持续风向微风':
        #                windD='无持续风向'
        #                windP='微风'
            if weatherClass=='tqshow7':

                if weather2.xpath('h3'):
                    day=weather2.xpath('h3/text()').extract()[0].strip()
                if weather2.xpath('ul[1]/li[2]'):
                    baitian=''
                    yejian=''
                    if weather2.xpath('ul[1]/li[2]/text()'):
                        baitian=weather2.xpath('ul[1]/li[2]/text()').extract()[0].strip()
                    if  weather2.xpath('ul[1]/li[3]/text()'):
                        yejian=weather2.xpath('ul[1]/li[3]/text()').extract()[0].strip()
                    if baitian==yejian:
                        weather=baitian
                    else:
                        weather=baitian+'~'+yejian
                    max=weather2.xpath('ul[1]/li[4]/font[1]/text()').extract()[0].strip()
                    min=weather2.xpath('ul[1]/li[4]/font[2]/text()').extract()[0].strip()
                    wind=''
                    windD=''
                    windP=''
                    if weather2.xpath('ul[1]/li[5]/text()'):
                        wind=weather2.xpath('ul[1]/li[5]/text()').extract()[0].strip()
                    if len(wind.split(' '))>=2:
                        windD=wind.split(' ')[0]
                        windP=wind.split(' ')[1]
                    if wind=='无持续风向微风':
                        windD='无持续风向'
                        windP='微风'

            item=WeatherItem()
            item['provinceId']=itemtmp['provinceId']
            item['province']=itemtmp['province']
            item['cityId']=itemtmp['cityId']
            item['city']=itemtmp['city']
            item['countyId']=itemtmp['countyId']
            item['county']=itemtmp['county']
            item['month']=itemtmp['month']
            item['day']=self.year+'-'+day.replace('（周一）','').replace('（周二）','').replace('（周三）','').replace('（周四）','').replace('（周五）','').replace('（周六）','').replace('（周日）','').replace('月','-').replace('日','').strip()
            item['max']=max
            item['min']=min
            item['weather']=weather
            item['windD']=windD
            item['windP']=windP
            items.append(item)

        return items

