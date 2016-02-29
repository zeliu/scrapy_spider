#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import random
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector
import sys
#---------------------------------------------------------------------------
class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "mt"
    allowed_domains = ["meituan.com"]
    download_delay = 0.7
    start_urls = [
        "http://i.meituan.com/select/beijing/page_1.html"
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
        '下一页地址'
        next_list = sel.xpath('//*[@class="pager"]/a')
        #print 'ad:'+str(next_list[0].xpath('text()').extract()[0].encode('utf-8'))
        for page in next_list:
            if page.xpath('text()').extract()[0].encode('utf-8')=='下一页':
                url =  page.xpath('@href').extract()[0].split('=')[-1]
                print '--------afag----------'+url
                ua = random.choice(self.user_agent_list)
                if ua:
                    print 'useragent-111------------'+ua
                    r = Request('http://i.meituan.com/select/beijing/page_'+str(url)+'.html', callback=self.parse)
                    r.headers.setdefault('User-Agent', ua)
                    req.append(r)

        '商铺详情页'
        shop_list = sel.xpath('//*[@class="list"]/dd')
        saleNum_list=sel.xpath('//*[@class="list"]/dd//*[@class="line-right"]')
        for i in range(len(shop_list)):
            url=shop_list[i].xpath('a[1]/@href').extract()[0]
            price=shop_list[i].xpath('a[1]/div[1]/div[2]/div[3]/span[1]/text()').extract()[0]
            saleNum=saleNum_list[i].xpath('text()').extract()[0]
            print '------nexturl:---------'+str(url)
            ua = random.choice(self.user_agent_list)
            if ua:
                r = Request(url, callback=self.parse_nextpage)
                print 'useragent-222------------'+ua
                item = TutorialItem()
                item['price']=price.strip()
                item['saleNum']=saleNum.replace('已售','').strip()
                r.meta['item'] = item
                r.headers.setdefault('User-Agent', ua)
                req.append(r)
        return req

    def parse_nextpage(self,response):
        req = []
        sel = Selector(response)
        #print(response.body)
        '下一页地址'
        next_list = sel.xpath('//*[@class="pull-right "]/text()').extract()#[0].replace('人评价','')
        next_list2 = sel.xpath('//*[@class="pull-right"]/text()').extract()

        if next_list2:
            total=next_list2[0].replace('人评价','')
        if next_list:
            total=next_list[0].replace('人评价','')
        #total=int(next_list)/15+1
        shopid=sel.xpath('/html/head/link[4]/@href').extract()[0].split('/')[-1].split('.')[0]
        print '-----dafaaaaaaaaaaaaaa:---'+str(total)
        item = response.meta['item']
        tag_list=sel.xpath('//*[@class="tag-category"]/span[1]/text()').extract()
        tag=''
        for tags in tag_list:
            if tag=='':
                tag=tags
            tag=tag+'|'+tags
        for page in range(int(total)/15+1):
            url =  'http://i.meituan.com/deal/'+str(shopid)+'/feedback/page_'+str(page+1)
            print '--------afag2:----------'+url
            ua = random.choice(self.user_agent_list)
            if ua:
                r = Request(url, callback=self.parse_comments)
                print 'useragent-333------------'+ua
                r.headers.setdefault('User-Agent', ua)
                item['url']=url.strip()
                item['tag']=tag.strip()
                r.meta['item'] = item
                req.append(r)
        return req


    def parse_comments(self,response):

        '获取评价信息'
        sel = Selector(response)
        items = []
        #shopid=sel.xpath('//*[@class="revitew-title"]/h1[1]/a[1]/@href').extract()
        shopname=sel.xpath('//*[@class="feedbackCard"]/div[4]/weak[1]/text()').extract()
        #userid=sel.xpath('//*[@class="pic"]/a[1]/@user-id').extract()
        name=sel.xpath('//*[@class="username"]/text()').extract()
        score=sel.xpath('//*[@class="stars"]')#.extract()
        comment=sel.xpath('//*[@class="comment"]')#.extract()
        #brand_name=sel.xpath('//*[@class="misc-name"]/text()').extract()
        time=sel.xpath('//*[@class="time"]/text()').extract()
        itemtmp = response.meta['item']
        for i in range(len(name)):
            item = TutorialItem()
            #item['store_id'] = shopid[0].split('/')[-1].strip()
            item['store_name'] = shopname[0].strip()
            item['name'] = name[i].strip()
            item['price']=itemtmp['price']
            item['saleNum']=itemtmp['saleNum']
            item['tag']=itemtmp['tag']
            item['url']=itemtmp['url']
            #item['brand_name'] = brand_name[i].strip()
            s_list=score[i].xpath('i/@class').extract()
            s_score=0
            for stars in s_list:
                if stars=='text-icon icon-star':
                    s_score=s_score+1
            item['score'] = s_score#str(len(score[i].xpath('i/@class').extract()))
            #item['userid'] = userid[i].strip()
            item['time'] = time[i].strip()
            comsize=comment[i].xpath('p[1]/text()').extract()
            if comsize:
                item['comment'] = comment[i].xpath('p[1]/text()').extract()[0].strip().replace('\n','').replace('\r','')
            items.append(item)
        #item = response.meta['item']

        return items
        ############################################################################