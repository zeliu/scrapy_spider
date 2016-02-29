#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import PlazaItem
from tutorial.items import PlazaShop
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
import urllib
import urllib2
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "baidu_pic_plaza"
    download_delay = 3
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/plaza")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        arr=line.split('\t')
        wandaPlazaName=arr[0]
        plazaUrl=arr[1]

        start_urls.append(plazaUrl.strip())
    #start_urls=['http://image.baidu.com/search/index?tn=baiduimage&word=%E5%8C%97%E4%BA%AC%E9%87%91%E5%9C%B0%E4%B8%AD%E5%BF%83+%E5%AE%A4%E5%86%85']



    def parse(self, response):
        '获取商铺详情页'
        req=[]
        sel = Selector(response)
        plazaId=response.url.split('/')[-1]
        plazaCity=sel.xpath('//*[@class="city J-city"]/text()').extract()[0].strip()
        plazaName=''
        if sel.xpath('//*[@class="market-name"]/text()'):
            plazaName=sel.xpath('//*[@class="market-name"]/text()').extract()[0].strip()
        item1=PlazaItem()
        item1['plazaId']=plazaId
        item1['plazaCity']=plazaCity
        url='http://image.baidu.com/search/index?tn=baiduimage&word='+plazaCity+' '+plazaName+' 室内'
        item1['picType']='室内'
        r = Request(url, callback=self.parse_pic)
        r.meta['item'] = item1
        item2=PlazaItem()
        item2['plazaId']=plazaId
        item2['plazaCity']=plazaCity
        url2='http://image.baidu.com/search/index?tn=baiduimage&word='+plazaCity+' '+plazaName+' 室外'
        item2['picType']='室外'
        r2 = Request(url2, callback=self.parse_pic)
        r2.meta['item'] = item2
        req.append(r)
        req.append(r2)
        return req

    def parse_pic(self, response):
        '获取商铺详情页'

        htmlbody= str(response.body).replace('\n','').replace('\r','')
        itemtmp = response.meta['item']
        #picRule=re.compile(r"(.*?)(\"objURL\":\")(.*?)(jpg\",)")
        picRule=re.compile(r"(.*?)(app.setData\(\'imgData\',)(.*?)(\);)")
        #urltmp=picRule.findall(htmlbody.encode('UTF-8'))#.group(3)
        urlttmp=picRule.match(htmlbody.encode('UTF-8'))
        urljson= urlttmp.group(3)
        s=json.loads(str(urljson))
        piclist= s['data']
        img=[]
        for i in range(len(piclist)):
            if i<20:
                img.append(piclist[i]['objURL'])

        item=PlazaItem()

        item['image_urls']=img
        item['plazaId']=itemtmp['plazaId']
        item['picType']=itemtmp['picType']
        return item







