#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import json
from tutorial.items import TeleplayItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    #sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "iqiyi"
    allowed_domains = ["iqiyi.com"]

    start_urls = [
        "http://list.iqiyi.com/www/2/-------------11-1-1-iqiyi--.html"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        sel = Selector(response)
        year_list = sel.xpath('//*[@class="mod_sear_list borNone"]/ul/li/a')
        for i in range(len(year_list)):
            if i!=0:
                url='http://list.iqiyi.com'+year_list[i].xpath('@href').extract()[0]
                year=year_list[i].xpath('text()').extract()[0]
                print url
                item = TeleplayItem()
                item['year']=year.strip()
                r = Request(url, callback=self.parse_nextpage)
                r.meta['item'] = item
                req.append(r)
        return req

    def parse_nextpage(self,response):
        req = []
        sel = Selector(response)
        '下一页地址'
        itemtmp=response.meta['item']

        total=1
        if sel.xpath('//*[@class="mod-page"]/a/@data-key').extract():
            total = sel.xpath('//*[@class="mod-page"]/a/@data-key').extract()[-2]
        urltmp=response.url
        if total:
            for i in range(int(total)):
                url=urltmp.replace('11-1-1','11-'+str(i+1)+'-1')
                r = Request(url, callback=self.parse_list)
                r.meta['item'] = itemtmp
                req.append(r)
        return req

    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '电影列表'
        itemtmp=response.meta['item']
        movie_list = sel.xpath('//*[@class="site-piclist_info_title"]/a')
        for i in range(len(movie_list)):
            url=movie_list[i].xpath('@href').extract()[0]
            print '------url:---------'+str(url)
            r = Request(url, callback=self.parse_detail)
            item = TeleplayItem()
            item['year']= itemtmp['year']
            item['name']= movie_list[i].xpath('@title').extract()[0].strip()
            item['episode']=sel.xpath('//*[@class="textOverflow"]/text()').extract()[i].strip()
            r.meta['item'] = item
            req.append(r)
        return req



    def parse_detail(self,response):

        '电影详情'
        sel = Selector(response)
        #items = []
        item = TeleplayItem()
        itemtmp=response.meta['item']
        #name=sel.xpath('//*[@class="white"]/text()').extract()[0]
        #episode=''
        #if sel.xpath('//*[@style="margin-top:-2px;"]/text()').extract():
        #    episode=sel.xpath('//*[@style="margin-top:-2px;"]/text()').extract()[0]
        #if  sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]').extract():
        #    if sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/a[1]/text()').extract():
        #        episode=sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/a[1]/text()').extract()[0]
        #        if '更新' in sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/a[1]/text()').extract()[0]:
        #            episode=sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/text()').extract()[0]
        #        if '总集数' in sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/text()').extract()[0]:
        #            episode=sel.xpath('//*[@class="topic_item clearfix"][4]/div[1]/em[1]/text()').extract()[0]
        area=''
        if sel.xpath('//*[@class="topic_item clearfix"][2]/div[2]/em[1]/a/text()').extract():
            area=sel.xpath('//*[@class="topic_item clearfix"][2]/div[2]/em[1]/a/text()').extract()[0]
        if sel.xpath('//*[@class="mini-block fl"][1]/p[1]/a[1]/text()').extract():
            area=sel.xpath('//*[@class="mini-block fl"][1]/p[1]/a[1]/text()').extract()[0]
        language=''
        if sel.xpath('//*[@class="mini-block fl"][1]/p[2]/a[1]/text()').extract():
            language=sel.xpath('//*[@class="mini-block fl"][1]/p[2]/a[1]/text()').extract()[0]
        if sel.xpath('//*[@class="topic_item clearfix"][3]/div[2]/em[1]/a/text()').extract():
            language=sel.xpath('//*[@class="topic_item clearfix"][3]/div[2]/em[1]/a/text()').extract()[0]
        directer_list=[]
        if sel.xpath('//*[@class="mini-block fl"][2]/p[1]/a/text()').extract():
            directer_list=sel.xpath('//*[@class="mini-block fl"][2]/p[1]/a/text()').extract()
        if sel.xpath('//*[@class="topic_item clearfix"][2]/div[1]/em[1]/a/text()').extract():
            directer_list=sel.xpath('//*[@class="topic_item clearfix"][2]/div[1]/em[1]/a/text()').extract()
        directer=''
        for directertmp in directer_list:
            directer=directer+'/'+directertmp.strip()

        type_list=[]
        if sel.xpath('//*[@class="topic_item clearfix"][3]/div[1]/em[1]/a/text()').extract():
            type_list=sel.xpath('//*[@class="topic_item clearfix"][3]/div[1]/em[1]/a/text()').extract()
        if sel.xpath('//*[@class="large-block fl"]/p[1]/a/text()').extract():
            type_list=sel.xpath('//*[@class="large-block fl"]/p[1]/a/text()').extract()
        type=''
        for typetmp in type_list:
            type=type+'/'+typetmp.strip()

        actor_list=[]
        if sel.xpath('//*[@class="large-block fl"]/p[2]/a/text()').extract():
            actor_list=sel.xpath('//*[@class="large-block fl"]/p[2]/a/text()').extract()
        if sel.xpath('//*[@class="topic_item clearfix"][1]/div[1]/em[1]/a/text()').extract():
            actor_list=sel.xpath('//*[@class="topic_item clearfix"][1]/div[1]/em[1]/a/text()').extract()
        actor=''
        for actortmp in actor_list:
            actor=actor+'/'+actortmp.strip()
        playCnts=sel.xpath('//*[@id="widget-playcount"]/text()').extract()[0]
        id=0
        if sel.xpath('//*[@data-widget-upanddown="upanddown"]/@data-upanddown-albumid').extract():
            id=sel.xpath('//*[@data-widget-upanddown="upanddown"]/@data-upanddown-albumid').extract()[0].strip()
        if sel.xpath('//*[@id="upDownWrap"]/@data-qpaid').extract():
            id=sel.xpath('//*[@id="upDownWrap"]/@data-qpaid').extract()[0].strip()
        #dislikeCnts=sel.xpath('//*[@id="widget-votedown"]/text()').extract()[0]

        item['name'] = itemtmp['name']
        item['episode'] = itemtmp['episode']
        item['area'] = area.strip()
        item['language'] = language.strip()
        item['directer']=directer[1:].strip()
        item['type']=type[1:].strip()
        item['actor']=actor[1:].strip()
        item['playCnts']=playCnts.strip()
        item['id'] = id.strip()
        #item['likeCnts']=likeCnts.strip()
        #item['dislikeCnts']=dislikeCnts.strip()
        item['year']=itemtmp['year']
        url='http://up.video.iqiyi.com/ugc-updown/quud.do?dataid='+str(id)+'&type=1'
        r = Request(url, callback=self.parse_updown)
        r.meta['item'] = item
        return r

    def parse_updown(self,response):
        #items = []
        item=response.meta['item']
        mystr=str(response.body).replace('try{null(','').replace(')}catch(e){}','')
        print '**************'+mystr
        s=json.loads(mystr)
        item['likeCnts']=str(s['data']['up']).strip()
        item['dislikeCnts']=str(s['data']['down']).strip()

        return item