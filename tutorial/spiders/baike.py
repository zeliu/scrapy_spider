#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
from tutorial.items import Baike
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "baike"
    download_delay = 0.3
    allowed_domains = ["baike.baidu.com"]
    start_urls=['http://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/114923']
    #for i in range(20):
    #    url='http://baike.baidu.com/view/'+str(i)+'.htm'
    #    start_urls.append(url)




    def parse(self, response):
        req=[]
        sel = Selector(response)
        item=self.parse_html(response)
        if sel.xpath('//*[@class="polysemantList-wrapper cmn-clearfix"]'):
            for url in sel.xpath('//*[@class="polysemantList-wrapper cmn-clearfix"]/li/a/@href').extract():
                r = Request('http://baike.baidu.com'+url, callback=self.parse_detail)
                r.meta['item'] = item
                req.append(r)
        else:
            req.append(item)
        return req

    def parse_detail(self, response):
        req=[]
        itemtmp = response.meta['item']
        req.append(itemtmp)
        item=self.parse_html(response)
        req.append(item)
        return req

    def parse_html(self,response):
        sel = Selector(response)
        item=Baike()
        title=sel.xpath('//*[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0].replace('\n','').replace('\r','').replace('\001','').replace('\"','\\"').strip()
        if sel.xpath('//*[@class="lemmaWgt-lemmaTitle-title"]/h2/text()'):
            title=title+sel.xpath('//*[@class="lemmaWgt-lemmaTitle-title"]/h2/text()').extract()[0].strip()
        item['keyword']=title.replace('\n','').replace('\r','').replace('\001','')

        context=sel.xpath('//*[starts-with(@class,"para")]|//*[starts-with(@class,"custom_dot")]|//*[starts-with(@class,"catalog-list")]')

        datas=context.xpath('string(.)').extract()
        links=context.xpath('descendant::a[contains(@href,"view")or starts-with(@href,"#")]').xpath('string(.)').extract()
        output=""
        outputlink=''
        s=set()
        for data in datas:
            output=output+data.replace('\n','').replace('\r','').replace('\001','').strip()
        for link in links:
            if link.strip()!='':
                s.add(link.strip())
        for t in s:
            outputlink=outputlink+t.replace('\002','')+'\002'
        open_tags=sel.xpath('//*[@id="open-tag-item"]').xpath('string(.)').extract()
        tags=''
        for tag in open_tags:
            if tag.strip()!='':
                tags=tags+tag.replace('\n','').replace('\r','').replace('\001','').strip()+'|'
        item['tags']=tags.replace('，',',')[:-1]
        item['context']=output
        item['linkword']=outputlink[:-1].replace('\n','').replace('\r','').replace('\001','')
        item['html']= response.body.replace('\n','').replace('\r','').replace('\001','')
        item['url']=response.url
        if sel.xpath('//*[@class="polysemantList-wrapper cmn-clearfix"]'):
            item['ismany']='1'
        else:
            item['ismany']='0'
        return item









