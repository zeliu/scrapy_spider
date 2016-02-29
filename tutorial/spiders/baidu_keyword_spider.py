#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import BaiduKeyWords
from tutorial.items import PlazaItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
import urllib
from twisted.internet import reactor
import urllib2
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "baidu_keyword"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=[]
    f = open("keyword/baidukeywords")
    for line in f:

        #str=urllib.quote(line.decode('utf-8').encode('gbk'))
        urltmp="http://61.135.169.121/s?wd="+line.strip()+" 品牌"
        start_urls.append(urltmp)



    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        #keyWords=response.url.split('=')[-1].decode('utf-8')
        keyWords=urllib2.unquote(response.url.split('=')[-1]).encode('utf-8')
        nums=sel.xpath('//*[@class="nums"]/text()').extract()[0].strip()

        relation_list=sel.xpath('//*[@class="opr-recommends-merge-content"]/div')
        i=1
        brand=''
        for relations in relation_list:
            print 'i===:'+str(i)
            if relations.xpath('span[1]/text()'):
                if '品牌' in relations.xpath('span[1]/text()').extract()[0].strip():
                    print '$$$$$$$$$$$$:::'+relations.xpath('span[1]/text()').extract()[0].strip()
                    divcount=i+1
                    print str(divcount)
                    brands_list1=sel.xpath('//*[@class="opr-recommends-merge-content"]/div['+str(divcount)+']/div/div/div[2]/a[1]')
                    brands_list2=sel.xpath('//*[@class="opr-recommends-merge-content"]/div['+str(divcount)+']/div/div/div/div[2]/a[1]')
                    brands_list3=sel.xpath('//*[@class="opr-recommends-merge-content"]/div['+str(divcount)+']/div/div/div[2]/a[1]')

                    for brand1 in brands_list1:
                        brandtmp1=brand1.xpath('@title').extract()[0].strip()
                        brand=brand+'|'+brandtmp1
                    for brand2 in brands_list2:
                        brandtmp2=brand2.xpath('@title').extract()[0].strip()
                        brand=brand+'|'+brandtmp2
                    if  len(brands_list1)==0:
                        for brand3 in brands_list3:
                            brandtmp3=brand3.xpath('@title').extract()[0].strip()
                            brand=brand+'|'+brandtmp3
            i=i+1

        sousuo_list=sel.xpath('//*[@id="rs"]/table/tr')
        #brand_list1=sel.xpath('//*[@class="opr-recommends-merge-panel opr-recommends-merge-mbGap"][1]/div/div/div[2]/a[1]')
        #brand_list2=sel.xpath('//*[@class="opr-recommends-merge-panel opr-recommends-merge-mbGap"][1]/div/div/div/div[2]/a[1]')
        #brand_list3=sel.xpath('//*[@class="opr-recommends-merge-panel"][1]/div/div/div[2]/a[1]')

        item=BaiduKeyWords()
        tuijian=''
        for tr in sousuo_list:
            th_list=tr.xpath('th')#.extract()[0].strip()
            for th in th_list:
                if th.xpath('a/text()'):
                    tuijian=tuijian+'|'+th.xpath('a/text()').extract()[0].strip()

        item['keyWords']=keyWords
        item['nums']= nums.replace('百度为您找到相关结果约','').replace('个','').replace(',','')
        item['relationSearch'] =tuijian[1:]
        item['realationBrand'] =brand[1:]
        return item







