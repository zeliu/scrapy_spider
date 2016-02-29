#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
from tutorial.items import HotelItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
import datetime

#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "elongnew"
    #allowed_domains = ["elong.com"]
    download_delay = 0.5
    #DUPEFILTER_DEBUG=true
    dupefilter_debug=True
    start_urls = [
        "http://m.elong.com"
    ]
    def get_day(self,day):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=day)
        return tomorrow


    def parse(self, response):
        '获取商铺详情页'
        req = []
        holtel_list=["北京万达索菲特-beijing-50101461","北京万达嘉华-beijing-40601023","哈尔滨万达索菲特-harbin-41001032","宁波万达索菲特-ningbo-51202013","成都万达索菲特-chengdu-52301011","长白山万达宜必思-chixi-30914080","潍坊万达铂尔曼-weifang-90187438","青岛万达艾美-qingdao-51601030","重庆万达艾美-chongqing-50401032","无锡万达喜来登-wuxi-51105020","福州万达威斯汀-fuzhou-51402017","合肥万达威斯汀-hefei-51301014","武汉万达威斯汀-wuhan-51801039","镇江万达喜来登-zhenjiang-51108004","大庆万达喜来登-daqing-51004002","常州万达喜来登-changzhou-51103009","长白山威斯汀-chixi-50914005","长白山喜来登-chixi-50914006","宜兴万达艾美-yixing-51109007","襄阳万达皇冠假日-xiangyang-51804002","宜昌万达皇冠假日-yichang-51803003","石家庄万达洲际-shijiazhuang-50501012","唐山万达洲际-tangshan-50101635","长白山假日酒店-chixi-40914008","长白山假日套房-chixi-40914009","长白山万达智选假日-chixi-30909002","三亚万达康莱德-sanya-52201183","三亚万达逸林-sanya-52201182","西安万达希尔顿-xian-52701044","广州万达希尔顿-guangzhou-52001128","南京万达希尔顿-nanjing-51101041","泰州万达逸林-taizhou-51115002","大连万达康莱德-dalian-50801068","大连万达希尔顿-dalian-50801069","万州万达逸林-wanzhou-50401127","济南万达凯悦-jinan-51602018","长白山万达柏悦-chixi-50914027","长白山万达凯悦-chixi-50914026","武汉万达瑞华-wuhan-51801139","太原万达文华-taiyuan-50601022","泉州万达文华-quanzhou-51403004","长沙万达文华-changsha-51901054","沈阳万达文华-shenyang-50802095","天津万达文华-tianjin-50301169","东莞万达文华-dongguan-90531923","兰州万达文华-lanzhou-90577970","昆明万达文华-kunming-90541428","烟台万达文华-yantai-90305081","廊坊万达嘉华-langfang-00511019","宁德万达嘉华-ningde-51414001","漳州万达嘉华-zhangzhou-51408003","淮安万达嘉华-huaian-51123005","抚顺万达嘉华-fushun-50804002","武汉万达嘉华-wuhan-51801088","哈尔滨万达嘉华-harbin-51001038","南昌万达嘉华-nanchang-51501037","银川万达嘉华-yinchuan-52901017","丹东万达嘉华-dandong-50806005","南京万达嘉华-nanjing-51101150","广州增城万达嘉华-guangzhou-90122524","赤峰万达嘉华-chifeng-90245952","济宁万达嘉华-jining-90220994","金华万达嘉华-jinhua-90323745","常州万达嘉华-changzhou-90212821","马鞍山万达嘉华-maanshan-90420053","荆州万达嘉华-jingzhou-90333648","龙岩万达嘉华-longyan-90563036","江门万达嘉华-jiangmen-90636488","芜湖万达嘉华-wuhu-90635067","蚌埠万达嘉华-bengbu-90656677","南宁万达文华-nanning-90556321","广元万达嘉华-guangyuan-90840020","内江万达嘉华-neijiang-90877980","黄石万达嘉华-huangshi-90871978","安阳万达嘉华-anyang-90916862","东营万达嘉华-dongying-90927387","泰安万达嘉华-taian-90907902","西双版纳万达文华-xishuangbanna-90946681","呼和浩特万达文华酒店-hohhot-91007594","柳州万达嘉华酒店-liuzhou-90959432"]
        #holtel_list=["北京万达索菲特-beijing-50101461"]
        for hotel in holtel_list:
            hotelId=hotel.split('-')[2]
            hotelName=hotel.split('-')[0]
            city=hotel.split('-')[1]
            for j in range(30):
                #print j
                item =HotelItem()
                item['hotelName']=hotelName
                item['hotelId']=hotelId
                today=self.get_day(j)
                tomorrow=self.get_day(j+1)
                url='http://m.elong.com/hotel/api/hoteldetailroomlist/?indate='+str(today)+'&outdate='+str(tomorrow)+'&hotelid='+hotelId
                #print url
                r = Request(url, callback=self.parse_hotel)
                item['inDate']=str(today)
                r.meta['item'] = item
                req.append(r)
        return req

    def parse_hotel(self, response):
        '获取商铺详情页'
        items=[]
        itemtmp = response.meta['item']
        s=json.loads(response.body)
        for roomInfo in s['roomInfoList']:
            roomInfoName=roomInfo['roomInfoName']
            rpList=roomInfo['rpList']
            for rp in rpList:
                item=HotelItem()
                item['roomType']= roomInfoName

                item['hotelId']=itemtmp['hotelId']
                item['hotelName']=itemtmp['hotelName']
                item['inDate']=itemtmp['inDate']
                item['source']='艺龙'
                productName=rp['productName']
                item['priceType']=productName
                averagePrice=rp['averagePrice']
                item['priceBefore']=str(averagePrice)
                averagePriceSubTotal=rp['averagePriceSubTotal']
                item['priceAfter']=str(averagePriceSubTotal)
                additionList=rp['additionInfoList']
                cancelType=rp['cancelType']
                cancel='免费取消'
                if cancelType==1:
                    cancel='限时取消'
                if cancelType==2:
                    cancel='不可取消'
                item['policy']=cancel
                showPayType=rp['showPayType']
                paytype='到店付'
                if showPayType==1:
                    paytype='担保'
                if showPayType==2:
                    paytype='预付'
                item['type']= paytype
                for addition in additionList:
                    key=addition['key']
                    if key=='breakfast':
                        brea=addition['content']
                        item['breakfast']= brea
                items.append(item)
        return items


