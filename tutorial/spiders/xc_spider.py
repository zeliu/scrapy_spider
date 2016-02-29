#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import HotelItem
from scrapy import Request
import datetime
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "ctrip"
    allowed_domains = ["ctrip.com"]

    start_urls = [
        "http://m.ctrip.com"
    ]
    def get_day(self,day):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=day)
        return tomorrow

    def parse(self, response):
        '获取商铺详情页'
        req = []
        url='http://m.ctrip.com/restapi/soa2/10933/hotel/product/roomgetv2?_fxpcqlniredt=09031141310038542730'
        hotel_list=["北京万达索菲特-375511","北京万达嘉华-430004","哈尔滨万达索菲特-430143","宁波万达索菲特-369761","成都万达索菲特-416176","长白山万达宜必思-548153","潍坊万达铂尔曼-962809","青岛万达艾美-393099","重庆万达艾美-396484","无锡万达喜来登-369725","福州万达威斯汀-430368","合肥万达威斯汀-419898","武汉万达威斯汀-371169","镇江万达喜来登-346296","大庆万达喜来登-430330","常州万达喜来登-347237","长白山威斯汀-427093","长白山喜来登-427096","宜兴万达艾美-473238","襄阳万达皇冠假日-396393","宜昌万达皇冠假日-425211","石家庄万达洲际-419300","唐山万达洲际-430264","长白山假日酒店-427100","长白山万达智选假日-546163","三亚万达康莱德-372203","三亚万达逸林-345069","西安万达希尔顿-371197","广州万达希尔顿-346487","南京万达希尔顿-369707","泰州万达逸林-367942","大连万达康莱德-400109","大连万达希尔顿-371180","万州万达逸林-514989","济南万达凯悦-425374","长白山万达柏悦-471944","武汉万达瑞华-712581","太原万达文华-483556","泉州万达文华-435646","长沙万达文华-386624","沈阳万达文华-474000","天津万达文华-531644","东莞万达文华-1111219","兰州万达文华-1250132","昆明万达文华-1198192","烟台万达文华-1293830","廊坊万达嘉华-425601","宁德万达嘉华-435940","漳州万达嘉华-432087","淮安万达嘉华-426562","抚顺万达嘉华-691646","武汉万达嘉华-480200","哈尔滨万达嘉华-512359","南昌万达嘉华-684322","银川万达嘉华-682786","丹东万达嘉华-668037","南京万达嘉华-670019","广州增城万达嘉华-850467","赤峰万达嘉华-1008683","济宁万达嘉华-980063","金华万达嘉华-1006218","常州万达嘉华-1008718","马鞍山万达嘉华-1225627","荆州万达嘉华-1372562","龙岩万达嘉华-1372535","江门万达嘉华-1198068","芜湖万达嘉华-1487247","蚌埠万达嘉华-1440500"]
        for hotel in hotel_list:
            hotelId=hotel.split('-')[1]
            hotelName=hotel.split('-')[0]
            item =HotelItem()
            item['hotelName']=hotelName
            item['hotelId']=hotelId
            for i in range(30):
                today=self.get_day(i)
                tomorrow=self.get_day(i+1)
                tbody='{"ver":0,"id":'+str(hotelId)+',"inDay":"'+str(today)+'","outDay":"'+str(tomorrow)+'","contrl":8,"num":1,"flag":512,"sf":1,"pay":0,"membertype":"","anony":true,"head":{"cid":"09031141310038542730","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":null},"contentType":"json"}'
                r = Request(url,method='POST',body=tbody,callback=self.parse_hotel)
                item['inDate']=str(today)
                r.meta['item'] = item
                req.append(r)
        return req
    def parse_hotel(self, response):
        '获取商铺详情页'
        items=[]
        itemtmp = response.meta['item']
        s=json.loads(response.body)
        hotelId= s['htl']
        rooms=s['rooms']
        for room in rooms:
            item=HotelItem()
            item['hotelId']=hotelId
            item['source']='携程'
            item['roomType']=room['bname']
            item['priceType']=room['name']
            item['inDate']=itemtmp['inDate']
            item['hotelId']=itemtmp['hotelId']
            item['hotelName']=itemtmp['hotelName']
            priceBefore=0
            for totalprice in room['totalprice']:
                if totalprice['type']==1:
                    priceBefore=totalprice['amount']
            priceAfter=room['coninfo']['conprice']
            if priceAfter==0:
                priceAfter=priceBefore
            item['priceBefore']=priceBefore
            item['priceAfter']=priceAfter

            for basic in room['basicinfos']:
                if basic['type']==1:
                    item['breakfast']=basic['value']
                if basic['type']==23:
                    item['band']=basic['value']
                if basic['type']==3:
                    item['policy']=basic['value']
                if basic['type']==2:
                    item['bedType']=basic['value']
            type=room['pay']
            item['type']='到店付'
            if type==1:
                item['type']='担保'
            if type==0:
                item['type']='预付'
            items.append(item)
        return items