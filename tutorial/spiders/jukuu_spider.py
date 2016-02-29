#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import urllib
from tutorial.items import JukuuTranslate
from scrapy import Request
from scrapy.selector import Selector
import sys
import datetime
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "jukuu"
    download_delay = 0.3
    #allowed_domains = ["3.cn"]

    start_urls=[]
    f = open("keyword/translate_zh")
    for line in f:
        urltmp="http://www.jukuu.com/search.php?q="+line.strip()
        start_urls.append(urltmp)



    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        keyword=response.url.split("q=")[-1]
        item=JukuuTranslate()
        item['keyword']=urllib.unquote(keyword)

        if sel.xpath('//*[@align="center"]'):
            page_sign=sel.xpath('//*[@align="center"]/a/text()')
            if page_sign:
                total=len(page_sign)
            else:
                total=1
            for page in range(total):
                url="http://www.jukuu.com/show-"+keyword+"-"+str(page)+".html"
                r = Request(url,callback=self.parse_translate)
                r.meta['item'] = item
                req.append(r)
        return req

    def parse_translate(self, response):
        '获取商铺详情页'
        req=[]
        sel = Selector(response)
        itemtmp = response.meta['item']
        translate_list=sel.xpath('//*[@id="Table1"]/tr/td[1]/table/tr')
        for translate in translate_list:
            if translate.xpath('@class'):
                langeType=translate.xpath('@class').extract()[0]
                if langeType=='e':
                    item=JukuuTranslate()
                    item['keyword']=itemtmp['keyword']
                    english=translate.xpath('td[2]').extract()[0].replace('"','').replace('<td>','').replace('<b>','').replace('</b>','').replace('</td>','').strip()
                    item['en']=english
                if langeType=='c':
                    chinese=translate.xpath('td[2]').extract()[0].replace('"','').replace('<td>','').replace('<b>','').replace('</b>','').replace('</td>','').strip()
                    item['zh']=chinese
                    req.append(item)

        return req







