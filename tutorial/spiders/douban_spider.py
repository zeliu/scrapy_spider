#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import FilmItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "douban"
    allowed_domains = ["douban.com"]

    start_urls = [
        "http://movie.douban.com/tag/"
    ]


    def parse(self, response):

        '获取所有分类页'
        req = []
        sel = Selector(response)
        year_list = sel.xpath('//*[@class="tagCol"][4]/tbody/tr/td/a/text()').extract()
        for year in year_list:
            print year
            url='http://www.douban.com/tag/'+year.strip()+'/movie'
            print url
            item = FilmItem()
            item['year']=year.strip()
            r.meta['item'] = item
            r = Request(url, callback=self.parse_list)
            req.append(r)
        return req


    def parse_list(self, response):
        req = []
        sel = Selector(response)
        '下一页地址'
        next_list = sel.xpath('//*[@class="next"]')
        item=response.meta['item']
        url =  next_list.xpath('a[1]/@href').extract()[0]
        print '--------nexturl----------'+url
        r = Request('http://www.douban.com/tag/'+item['year']+'/movie'+str(url), callback=self.parse_list)
        req.append(r)

        '电影列表'
        movie_list = sel.xpath('//*[@class="mod movie-list"]/dl/dd')
        for movie in movie_list:
            url=movie.xpath('a[1]/@href').extract()[0]
            print '------url:---------'+str(url)
            r = Request(url, callback=self.parse_detail)
            req.append(r)
        return req



    def parse_detail(self,response):

        '电影详情'
        sel = Selector(response)
        #items = []
        item = FilmItem()
        text= sel.xpath('//*[@class="rating_wrap clearbox"]/text()').extract()
        rate_list=["lingjian","tuijian","haixing","jiaocha","hencha"]
        i=0
        for texts in text:
            if '%' in texts:
                item[rate_list[i]] = texts.strip()
                i=i+1

        score=sel.xpath('//*[@property="v:average"]/text()').extract()[0]
        counts=sel.xpath('//*[@property="v:votes"]/text()').extract()[0]
        moviename=sel.xpath('//*[@property="v:itemreviewed"]/text()').extract()[0]
        year=sel.xpath('//*[@class="year"]/text()').extract()[0]
        movieid=sel.xpath('/html/head/link[4]/@href').extract()[0].split('/')[-2]
        directer=sel.xpath('//*[@rel="v:directedBy"]/text()').extract()[0]
        bianju=sel.xpath('//*[@id="info"]/span[2]/span[2]/a[1]/text()').extract()[0]
        actors=sel.xpath('//*[@rel="v:starring"]/text()').extract()
        actor=''
        for actortmp in actors:
            actor=actortmp.strip()+'/'+actor
        genres=sel.xpath('//*[@property="v:genre"]/text()').extract()
        genre=''
        for genretmp in genres:
            genre=genretmp.strip()+'/'+genre

        rate_others=sel.xpath('//*[@class="rating_betterthan"]/a/text()').extract()
        rate_other=''
        for ratetmp in rate_others:
            rate_other=ratetmp.strip()+'|'+rate_other
        tags_list=sel.xpath('//*[@class="tags-body"]/a/text()').extract()
        tags=''
        for tagtmp in tags_list:
            tags=tagtmp.strip()+'|'+tags

        like_list=sel.xpath('//*[@class="recommendations-bd"]/dl/dd/a[1]/text()').extract()
        likes=''
        for liketmp in like_list:
            likes=liketmp.strip()+'|'+likes
        item['score'] = score
        item['counts'] = counts
        item['moviename'] = moviename.strip()
        item['movieid'] = movieid.strip()
        item['directer']=directer.strip()
        item['bianju']=bianju.strip()
        item['actor']=actor[:-1].strip()
        item['genre']=genre[:-1].strip()
        item['rate_other']=rate_other[:-1].strip()
        item['tags']=tags[:-1].strip()
        item['likes']=likes[:-1].strip()
        item['year']=year.strip()


        #items.append(item)
        return item

