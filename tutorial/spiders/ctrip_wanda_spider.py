#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import WandaLeyuan
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "wanda_leyuan"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]
    start_urls=["http://you.ctrip.com/sight/jinghong2154/1751577.html"]



    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        url="http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
        pagenum=sel.xpath('//*[@class="numpage"]/text()').extract()[0]
        for i in range(int(pagenum)):
            page=i+1
            mybody='poiID=23104123&districtId=2154&districtEName=Jinghong&pagenow='+str(page)+'&order=3.0&star=0&tourist=0&resourceId=1751577&resourcetype=2'
            r = Request(url,method='POST',body=mybody,callback=self.parse_comments,headers={"Content-Type":"application/x-www-form-urlencoded"})
            req.append(r)
        return req

    def parse_comments(self, response):
        '获取商铺详情页'
        req=[]
        sel = Selector(response)
        comment_list=sel.xpath('//*[@class="comment_ctrip"]/div')
        for comments in comment_list:
            com_classname=comments.xpath('@class').extract()[0].strip()
            if com_classname=='comment_single':
                username=comments.xpath('div[1]/span[1]/a[1]/@title').extract()[0].strip()
                in_list=comments.xpath('ul[1]/li')
                score=''
                comment=''
                time=''
                jingse_score=''
                quwei_score=''
                xiangjia_score=''
                for ins in in_list:
                    classname=''
                    if ins.xpath('@class'):
                        classname=ins.xpath('@class').extract()[0].strip()
                    if classname=='title cf':
                        score=ins.xpath('span[1]/span[1]/span[1]/@style').extract()[0].strip().replace('width:','').replace('%;','')
                        allscore=ins.xpath('span[1]/span[2]/text()').extract()[0].strip()
                        scores=allscore.split('：')
                        for i in range(len(scores)):
                            if '景色' in scores[i]:
                                jingse_score=scores[i+1].strip()[0]
                            if '趣味' in scores[i]:
                                quwei_score=scores[i+1].strip()[0]
                            if '性价' in scores[i]:
                                xiangjia_score=scores[i+1].strip()[0]
                    if classname=='from_link':
                        time=ins.xpath('span[1]/span[1]/em[1]/text()').extract()[0].strip()
                    if classname=='main_con':
                        comment=ins.xpath('span[1]/text()').extract()[0].strip()



            item=WandaLeyuan()
            item['username']=username
            item['time']=time
            item['score']=score
            item['jingse']=jingse_score
            item['quwei']=quwei_score
            item['xingjiabi']=xiangjia_score
            item['comment']=comment

            req.append(item)


        return req







