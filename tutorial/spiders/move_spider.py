#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
import json
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "movie"
    allowed_domains = ["douban.com"]

    start_urls = [
        "http://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=最新&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=经典&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=华语&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=欧美&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=韩国&sort=recommend&page_limit=2000&page_start=0",
        "http://movie.douban.com/j/search_subjects?type=movie&tag=日本&sort=recommend&page_limit=2000&page_start=0"
    ]

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def parse(self, response):
        '获取商铺详情页'
        req = []
        sel = Selector(response)
        '商铺详情页'
        s = json.loads(response.body)
        movies=s["subjects"]
        for id in movies:
            url='http://movie.douban.com/subject/'+id["id"]
            ua = random.choice(self.user_agent_list)
            r = Request(url, callback=self.parse_comments)
            r.headers.setdefault('User-Agent', ua)
            req.append(r)
        return req



    def parse_comments(self,response):

        '获取评价信息'
        sel = Selector(response)
        #items = []
        score=sel.xpath('//*[@class="ll rating_num"]/text()').extract()[0]
        counts=sel.xpath('//*[@class="rating_wrap clearbox"]/p[2]/a[1]/span[1]/text()').extract()[0]
        moviename=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        movieid=sel.xpath('/html/head/link[4]/@href').extract()[0].split('/')[-2]
        tag_list=sel.xpath('//*[@class="tags-body"]/a/text()').extract()
        tags=''
        for str in tag_list:
            tags=tags+str+'|'
        item = TutorialItem()
        item['score'] = score
        item['counts'] = counts
        item['moviename'] = moviename.strip()
        item['movieid'] = movieid.strip()
        item['tags']=tags[:-1]
        #items.append(item)
        return item
        ############################################################################