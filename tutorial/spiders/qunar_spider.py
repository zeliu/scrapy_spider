#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import datetime
import StringIO,gzip
from tutorial.items import HotelItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "qunar"
    #download_delay = 0.3
    allowed_domains = ["qunar.com"]

    start_urls = [
        "http://touch.qunar.com"
    ]

    def get_day(self,day):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=day)
        return tomorrow
    def parse(self, response):
        '获取商铺详情页'
        req = []
        hotel_list=["北京万达索菲特-beijing_city-1919","北京万达嘉华-beijing_city-3738","哈尔滨万达索菲特-haerbin-33","宁波万达索菲特-ningbo-2398","成都万达索菲特-chengdu-73","长白山万达宜必思-baishan-3101","潍坊万达铂尔曼-weifang-4284","青岛万达艾美-qingdao-2598","重庆万达艾美-chongqing_city-2710","无锡万达喜来登-wuxi-3653","福州万达威斯汀-fuzhou_fujian-2539","合肥万达威斯汀-hefei-2283","武汉万达威斯汀-wuhan-5130","镇江万达喜来登-zhenjiang-2827","大庆万达喜来登-daqing-2325","常州万达喜来登-changzhou-4327","长白山威斯汀-baishan-3048","长白山喜来登-baishan-2776","宜兴万达艾美-wuxi-5777","襄阳万达皇冠假日-xiangfan-2159","宜昌万达皇冠假日-yichang-2299","石家庄万达洲际-shijiazhuang-3454","唐山万达洲际-tangshan-2708","长白山假日酒店-baishan-2758","长白山假日套房-baishan-2806","长白山万达智选假日-baishan-3102","三亚万达康莱德-sanya-7345","三亚万达逸林-sanya-6274","西安万达希尔顿-xian-6066","广州万达希尔顿-guangzhou-7962","南京万达希尔顿-nanjing-6024","泰州万达逸林-taizhou_jiangsu-2678","大连万达康莱德-dalian-4594","大连万达希尔顿-dalian-4595","万州万达逸林-chongqing_city-9169","济南万达凯悦-jinan-4192","长白山万达柏悦-baishan-3084","长白山万达凯悦-baishan-3093","武汉万达瑞华-wuhan-7475","太原万达文华-taiyuan-3598","泉州万达文华-quanzhou-3625","长沙万达文华-changsha-5183","沈阳万达文华-shenyang-5452","天津万达文华-tianjin_city-5699","东莞万达文华-dongguan-6418","兰州万达文华-lanzhou-5462","昆明万达文华-kunming-4824","烟台万达文华-yantai-8563","廊坊万达嘉华-langfang-3050","宁德万达嘉华-ningde-2673","漳州万达嘉华-zhangzhou-2747","淮安万达嘉华-huaian-14499","抚顺万达嘉华-fushun-2428","武汉万达嘉华-wuhan-6929","哈尔滨万达嘉华-haerbin-5069","南昌万达嘉华-nanchang-4054","银川万达嘉华-yinchuan-3192","丹东万达嘉华-dandong-2573","南京万达嘉华-nanjing-7658","广州增城万达嘉华-guangzhou-13048","赤峰万达嘉华-chifeng-2461","济宁万达嘉华-jining-4281","金华万达嘉华-jinhua-8727","常州万达嘉华-changzhou-5963","马鞍山万达嘉华-maanshan-2701","荆州万达嘉华-jingzhou-4532","龙岩万达嘉华-longyan-5826","江门万达嘉华-jiangmen-3791","芜湖万达嘉华-wuhu-3292","蚌埠万达嘉华-bangbu-2877","南宁万达文华-nanning-4715"]
        for hotel in hotel_list:
            hotelId=hotel.split('-')[2]
            hotelName=hotel.split('-')[0]
            city=hotel.split('-')[1]
            item =HotelItem()
            item['hotelName']=hotelName
            item['hotelId']=hotelId
            item['city']=city
            for i in range(30):
                today=self.get_day(i)
                tomorrow=self.get_day(i+1)
                url='http://touch.qunar.com/h5/hotel/hoteldetail?cityUrl='+city+'&checkInDate='+str(today)+'&checkOutDate='+str(tomorrow)+'&location=&seq='+city+'_'+str(hotelId)
                item['inDate']=str(today)
                item['tomorrow']=str(tomorrow)
                r = Request(url,callback=self.parse_hotel)
                r.meta['item'] = item
                req.append(r)
        return req

    def parse_hotel(self, response):
        '酒店详情'
        req = []
        sel=Selector(response)
        itemtmp = response.meta['item']
        room_list=sel.xpath('//*[@class="li2"]')
        for room in room_list:
            room= room.xpath('div[1]/@data-room').extract()[0].strip()
            today=itemtmp['inDate']
            tomorrow=itemtmp['tomorrow']
            url='http://touch.qunar.com/h5/hotel/hotelprice?checkInDate='+str(today)+'&checkOutDate='+str(tomorrow)+'&location=&seq='+itemtmp['city']+'_'+itemtmp['hotelId']+'&tpl=hotel.hotelPriceTpl&key=&room='+room
            r = Request(url,callback=self.parse_hotel_price)
            r.meta['item'] = itemtmp
            req.append(r)
        return req

    def parse_hotel_price(self, response):
        '房间价格详情'
        items = []
        #print response.body
        itemtmp = response.meta['item']
        sel=Selector(response)
        room_list=sel.xpath('/html/body/ul/li')
        otroom_list=sel.xpath('/html/body/ul/li//*[@class="otaName"]')
        roomdetail_list=sel.xpath('/html/body/ul/li//*[@class="qn_font12 qn_grey roomName"]')
        op_list=sel.xpath('/html/body/ul/li//*[@class="op text"]')
        for i in range(len(room_list)):
            item=HotelItem()
            item['hotelId']=itemtmp['hotelId']
            item['hotelName']=itemtmp['hotelName']
            item['inDate']=itemtmp['inDate']
            item['source']='去哪儿'
            item['roomType']= room_list[i].xpath('@data-name').extract()[0]
            item['priceAfter']= room_list[i].xpath('@data-showprice').extract()[0]
            item['website']=  otroom_list[i].xpath('@data-otaname').extract()[0]
            priceType=''
            if roomdetail_list[i].xpath('text()').extract():
                priceType=roomdetail_list[i].xpath('text()').extract()[0]
            item['priceType']=priceType

            type='到店付'
            if op_list[i].xpath('div[1]/text()').extract()[0]=='在线付':
                type= op_list[i].xpath('div[1]/text()').extract()[0]
            item['type'] =type
            breakfast='未知'
            if '无早'in priceType:
                breakfast='无早'
            if '2份早餐'in priceType:
                breakfast='双早'
            if '1份早餐'in priceType:
                breakfast='单早'
            if '单早'in priceType:
                breakfast='单早'
            if '不含早'in priceType:
                breakfast='无早'
            if '含双'in priceType:
                breakfast='双早'
            if '双早'in priceType:
                breakfast='双早'
            if '含单'in priceType:
                breakfast='单早'
            if '含早'in priceType:
                breakfast='含早'
            item['breakfast']=breakfast
            items.append(item)
        return items