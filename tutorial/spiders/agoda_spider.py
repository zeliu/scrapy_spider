import scrapy
import json
from tutorial.items import HotelItem
from scrapy import Request
from scrapy.selector import Selector
import sys

class DpSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #handle_httpstatus_list = [403]
    name = "agoda"
    allowed_domains = ["agoda.com"]

    start_urls = [
        "http://www.agoda.com/Home/Home/NewHomeSearch/17116934/1/3/8/8/1/zh-cn/CN/zh-cn?asq=jGXBHFvRg5Z51Emf%2FbXG4w%3D%3D"
    ]


    def parse(self, response):
        req = []
        url='http://www.agoda.com/Home/Home/NewHomeSearch/17116934/1/3/8/8/1/zh-cn/CN/zh-cn?asq=jGXBHFvRg5Z51Emf%2FbXG4w%3D%3D'
        tbody = "CurrentCountryID=0&SearchInput=%E6%AD%A6%E6%B1%89%E4%B8%87%E8%BE%BE%E5%98%89%E5%8D%8E%E9%85%92%E5%BA%97&SeachDefaultText=%E6%AD%A6%E6%B1%89&CheckInMonthYear=07-2015&CheckInDay=17&NightCount=1&SelectedGuestOption=2&SelectedRoomOption=1&SelectedAdultOption=2&SelectedChildrenOption=0&IsAutoCompleteEnabled=True&ActionForm=AutoComplete&CityId=5818&CityTranslatedName=0&CountryId=191&ObjectId=502463&PageTypeId=7&MappingTypeId=0&LastSearchInput=%E6%AD%A6%E6%B1%89&UserLatitude=0&UserLongtitude=0&UserCityID=0&IsHotel=true"
        r = Request(url,method='POST',body=tbody,callback=self.parse_hotel)
        req.append(r)
        return req
    def parse_hotel(self, response):
        req = []
        print response.body
        pass