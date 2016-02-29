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
    name = "plaza_dp"
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



    def parse(self, response):
        '获取商铺详情页'
        req = []

        sel = Selector(response)
        plazaId=response.url.split('/')[-1]
        plazaCity=sel.xpath('//*[@class="city J-city"]/text()').extract()[0].strip()
        plazaImage=[]

        if sel.xpath('//*[@class="photo-container"]/a[1]/img/@src'):
            plazaImage=sel.xpath('//*[@class="photo-container"]/a[1]/img/@src').extract()
        if sel.xpath('//*[@class="photos-container"]/div[1]/a[1]/img/@src'):
            plazaImage=sel.xpath('//*[@class="photos-container"]/div[1]/a[1]/img/@src').extract()
        if sel.xpath('//*[@class="market-logo"]/img/@src'):
            plazaImage=sel.xpath('//*[@class="market-logo"]/img/@src').extract()
        plazaName=''
        plazaTime=''
        #if sel.xpath('//*[@class="shop-name"]/text()'):
        #    plazaName=sel.xpath('//*[@class="shop-name"]/text()').extract()[0].strip()
        if sel.xpath('//*[@class="market-name"]/text()'):
            plazaName=sel.xpath('//*[@class="market-name"]/text()').extract()[0].strip()
        if  sel.xpath('//*[@class="market-detail"]/p[2]/text()[2]'):
            plazaTime=sel.xpath('//*[@class="market-detail"]/p[2]/text()[2]').extract()[0].strip()
        plazaAddress1=''
        plazaAddress2=''
        if  sel.xpath('//*[@class="market-detail"]/p[1]/a[1]/text()'):
            plazaAddress1=sel.xpath('//*[@class="market-detail"]/p[1]/a[1]/text()').extract()[0].strip()
            plazaAddress2=sel.xpath('//*[@class="market-detail"]/p[1]/text()[3]').extract()[0].strip()
        #else :
        #    plazaAddress1=sel.xpath('//*[@itemprop="locality region"]/text()').extract()[0].strip()
        #    plazaAddress2=sel.xpath('//*[@itemprop="street-address"]/@title').extract()[0].strip()
        plazaAddress=plazaAddress1+plazaAddress2
        plazaOther_list=sel.xpath('//*[@class="market-detail-other Hide"]/p')
        plazaTel=''
        #plazaScore=''
        #plazaProScore=''
        #plazaEnvScore=''
        #plazaServScore=''
        #plazaAvg=''
        recommentitems=''
        if sel.xpath('//*[@class="expand-info tel"]/text()'):
            plazaTel=sel.xpath('//*[@class="expand-info tel"]/text()').extract()[1].strip()

        for plazaStr in plazaOther_list:
            str=plazaStr.xpath('span[1]/text()').extract()[0]
            if str=='联系电话：':
                plazaTel=plazaStr.xpath('text()[2]').extract()[0].strip()
            #if str=='用户评级：':
            #    plazaScore=plazaStr.xpath('span[2]/@class').extract()[0].replace('mid-rank-stars mid-str','').replace(' item','').strip()
            #    plazaProScore=plazaStr.xpath('span[3]/text()').extract()[0].replace('产品','').strip()
            #    plazaEnvScore=plazaStr.xpath('span[4]/text()').extract()[0].replace('环境','').strip()
            #    plazaServScore=plazaStr.xpath('span[5]/text()').extract()[0].replace('服务','').strip()
            #if str=='人均消费：':
            #    plazaAvg=plazaStr.xpath('text()[2]').extract()[0].replace('¥','').strip()
            if str=='推荐产品：':
                recommend_list=plazaStr.xpath('span')
                for recommend in recommend_list:
                    if recommend.xpath('@class').extract()[0].strip()!='title':
                        if recommend.xpath('a[1]/text()'):
                            recommendstr=recommend.xpath('a[1]/text()').extract()[0].strip()#.encode('utf-8')
                            recommentitems=recommentitems+"|"+recommendstr
                        #if recommend.xpath('text()[2]'):
                        #    recommenditem['proScore']=recommend.xpath('text()[2]').extract()[0].replace('(','').replace(')','').strip()#.encode('utf-8')

        #plazacomment_list=sel.xpath('//*[@class="mod-title J-tab"]/a')
        #plazacomment='0'
        #for plazacomments in plazacomment_list:
        #    commnetstr=plazacomments.xpath('@data-type').extract()[0]
        #    if commnetstr=='all':
        #        plazacomment=plazacomments.xpath('span[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #plazaComment5star = '0'
        #plazaComment4star = '0'
        #plazaComment3star = '0'
        #plazaComment2star = '0'
        #plazaComment1star = '0'
        #if sel.xpath('//*[@data-value="5star"]/span[1]/text()'):
        #    plazaComment5star=sel.xpath('//*[@data-value="5star"]/span[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #if sel.xpath('//*[@data-value="4star"]/span[1]/text()'):
        #    plazaComment4star=sel.xpath('//*[@data-value="4star"]/span[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #if sel.xpath('//*[@data-value="3star"]/span[1]/text()'):
        #    plazaComment3star=sel.xpath('//*[@data-value="3star"]/span[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #if sel.xpath('//*[@data-value="2star"]/span[1]/text()'):
        #    plazaComment2star=sel.xpath('//*[@data-value="2star"]/span[1]/text()').extract()[0].replace('(','').replace(')','').strip()
        #if sel.xpath('//*[@data-value="1star"]/span[1]/text()'):
        #    plazaComment1star=sel.xpath('//*[@data-value="1star"]/span[1]/text()').extract()[0].replace('(','').replace(')','').strip()

        item=PlazaItem()
        item['plazaId']=plazaId
        item['plazaName']=plazaName.replace('\n','').replace('\r','')
        item['plazaCity']=plazaCity
        item['plazaAddress']=plazaAddress.replace('\n','').replace('\r','')
        item['plazaTel']=plazaTel.replace('\n','').replace('\r','')
        item['plazaTime']=plazaTime.replace('\n','').replace('\r','')
        #item['plazaScore']=plazaScore
        #item['plazaProScore']=plazaProScore
        #item['plazaEnvScore']=plazaEnvScore
        #item['plazaServScore']=plazaServScore
        #item['plazaAvg']=plazaAvg
        item['plazaRecommend']=recommentitems[1:].replace('\n','').replace('\r','')
        #item['plazaComment']=plazacomment
        #item['plazaComment5star']=plazaComment5star
        #item['plazaComment4star']=plazaComment4star
        #item['plazaComment3star']=plazaComment3star
        #item['plazaComment2star']=plazaComment2star
        #item['plazaComment1star']=plazaComment1star
        item['image_urls']=plazaImage
        item['plazaLogsTfsFile']='-999999'
        url='http://restapi.amap.com/v3/place/text?keywords='+plazaCity+'%20'+plazaName+'&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=131000&s=rsv3&platform=JS&logversion=2.0&sdkversion=1.2'
        r = Request(url, callback=self.get_poi)
        r.meta['item'] = item
        return r

    def get_poi(self, response):
        item = response.meta['item']
        s=json.loads(response.body)
        if s['pois']:
            item['plazaPOI']=s['pois'][0]['location']
            return item
        else:
            url='http://restapi.amap.com/v3/place/text?keywords='+item['plazaCity']+'%20'+item['plazaAddress']+'&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=131000&s=rsv3&platform=JS&logversion=2.0&sdkversion=1.2'
            r = Request(url, callback=self.get_poi_addr)
            r.meta['item'] = item
            return r
    def get_poi_addr(self, response):
        item = response.meta['item']
        s=json.loads(response.body)
        item['plazaPOI']=s['pois'][0]['location']
        return item







