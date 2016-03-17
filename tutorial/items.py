# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userid = scrapy.Field()
    store_name= scrapy.Field()
    store_id= scrapy.Field()
    name = scrapy.Field()
    brand_name = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()
    comment = scrapy.Field()
    counts = scrapy.Field()
    moviename = scrapy.Field()
    movieid = scrapy.Field()
    tags = scrapy.Field()
    first = scrapy.Field()
    second = scrapy.Field()
    third = scrapy.Field()
    itemthirdid = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    hpid = scrapy.Field()
    url=scrapy.Field()
    saleNum=scrapy.Field()
    tag=scrapy.Field()

class JDItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first = scrapy.Field()
    second = scrapy.Field()
    third = scrapy.Field()
    cats=scrapy.Field()
    url=scrapy.Field()
    brandName=scrapy.Field()
    skuId=scrapy.Field()
    url=scrapy.Field()
    price=scrapy.Field()
    unit=scrapy.Field()
    name=scrapy.Field()
    delprice=scrapy.Field()


class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tomorrow=scrapy.Field()
    inDate=scrapy.Field()
    hotelId=scrapy.Field()
    hotelName=scrapy.Field()
    source= scrapy.Field()
    roomType = scrapy.Field()
    priceType = scrapy.Field()
    bedType = scrapy.Field()
    breakfast=scrapy.Field()
    band=scrapy.Field()
    policy=scrapy.Field()
    priceAfter=scrapy.Field()
    priceBefore=scrapy.Field()
    type=scrapy.Field()
    website=scrapy.Field()
    city=scrapy.Field()


class DPItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first = scrapy.Field()
    second = scrapy.Field()
    third = scrapy.Field()
    url=scrapy.Field()
    shopId=scrapy.Field()
    shopName=scrapy.Field()
    star=scrapy.Field()
    commentCnts=scrapy.Field()
    avgPrice=scrapy.Field()
    tasteScore=scrapy.Field()
    surrScore=scrapy.Field()
    serviceScore=scrapy.Field()
    address=scrapy.Field()
    tel=scrapy.Field()
    feature=scrapy.Field()
    time=scrapy.Field()
    service=scrapy.Field()
    tag=scrapy.Field()
    dish=scrapy.Field()


class CommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    shopId=scrapy.Field()
    shopName=scrapy.Field()
    username=scrapy.Field()
    contribution=scrapy.Field()
    star=scrapy.Field()
    tasteScore=scrapy.Field()
    surrScore=scrapy.Field()
    serviceScore=scrapy.Field()
    comments=scrapy.Field()
    time=scrapy.Field()
    avg=scrapy.Field()
    shopStar=scrapy.Field()
    shopAvg=scrapy.Field()



class FilmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    score = scrapy.Field()
    counts = scrapy.Field()
    moviename = scrapy.Field()
    movieid = scrapy.Field()
    tags = scrapy.Field()
    lingjian = scrapy.Field()
    tuijian = scrapy.Field()
    haixing = scrapy.Field()
    jiaocha = scrapy.Field()
    hencha = scrapy.Field()
    directer=scrapy.Field()
    bianju=scrapy.Field()
    actor=scrapy.Field()
    genre=scrapy.Field()
    rate_other=scrapy.Field()
    likes=scrapy.Field()
    year=scrapy.Field()

class TeleplayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    score = scrapy.Field()
    counts = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    tags = scrapy.Field()
    episode  = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    directer=scrapy.Field()
    type=scrapy.Field()
    actor=scrapy.Field()
    playCnts=scrapy.Field()
    likeCnts=scrapy.Field()
    dislikeCnts=scrapy.Field()
    year=scrapy.Field()
    commentCnts=scrapy.Field()
    guanzhuCnts=scrapy.Field()
    scoreCnts=scrapy.Field()


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    provinceId = scrapy.Field()
    cityId = scrapy.Field()
    cityEng = scrapy.Field()
    countyId = scrapy.Field()
    month = scrapy.Field()
    day  = scrapy.Field()
    max = scrapy.Field()
    min = scrapy.Field()
    weather=scrapy.Field()
    windD=scrapy.Field()
    windP=scrapy.Field()


class MobileItem(scrapy.Item):

    province = scrapy.Field()
    city = scrapy.Field()
    mobile = scrapy.Field()


class PlazaItem(scrapy.Item):
    plazaId = scrapy.Field()
    plazaName = scrapy.Field()
    plazaCity = scrapy.Field()
    picType = scrapy.Field()
    shopStreet = scrapy.Field()
    shopsUrl = scrapy.Field()
    plazaAddress = scrapy.Field()
    plazaTime = scrapy.Field()
    plazaTel = scrapy.Field()
    plazaScore = scrapy.Field()
    plazaProScore = scrapy.Field()
    plazaEnvScore = scrapy.Field()
    plazaServScore = scrapy.Field()
    plazaRecommend = scrapy.Field()
    plazaAvg = scrapy.Field()
    plazaPOI = scrapy.Field()
    plazaLogo = scrapy.Field()
    plazaShop = scrapy.Field()
    plazaBrand = scrapy.Field()
    plazaComment = scrapy.Field()
    plazaComment5star = scrapy.Field()
    plazaComment4star = scrapy.Field()
    plazaComment3star = scrapy.Field()
    plazaComment2star = scrapy.Field()
    plazaComment1star = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    plazaLogsTfsFile = scrapy.Field()
    brandName = scrapy.Field()
    brandPic = scrapy.Field()



class PlazaRecommend(scrapy.Item):
    proName = scrapy.Field()
    proScore = scrapy.Field()

class PlazaShop(scrapy.Item):
    plazaId = scrapy.Field()
    shopId = scrapy.Field()
    shopName = scrapy.Field()
    shopComment = scrapy.Field()
    shopStar = scrapy.Field()
    shopAvg = scrapy.Field()
    shopScore1 = scrapy.Field()
    shopScore2 = scrapy.Field()
    shopScore3 = scrapy.Field()
    shopAddress = scrapy.Field()
    shopFloor = scrapy.Field()
    shopRoom = scrapy.Field()
    shopTel = scrapy.Field()
    shopTime = scrapy.Field()
    shopTag = scrapy.Field()
    shopRecommend = scrapy.Field()
    shopOtherName = scrapy.Field()
    shopImg = scrapy.Field()
    shopStreet = scrapy.Field()
    shopUrl = scrapy.Field()
    shopCatetory1 = scrapy.Field()
    shopCatetory2 = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class ShopTag(scrapy.Item):
    tagName = scrapy.Field()
    tagScore = scrapy.Field()

class ShopRecommend(scrapy.Item):
    recName = scrapy.Field()
    recScore = scrapy.Field()

class MyJsonEncoder(json.JSONEncoder ):
    def default(self, obj):
        if isinstance(obj, PlazaRecommend):
            return {"proName": obj['proName'], "proScore": obj['proScore']}
        if isinstance(obj, ShopTag):
            return {"tagName": obj['tagName'], "tagScore": obj['tagScore']}
        if isinstance(obj, ShopRecommend):
            return {"recName": obj['recName'], "recScore": obj['recScore']}
        return json.JSONEncoder.default(self, obj)


class BaiduKeyWords(scrapy.Item):
    keyWords = scrapy.Field()
    nums = scrapy.Field()
    relationSearch = scrapy.Field()
    realationBrand = scrapy.Field()

class PlazaList(scrapy.Item):
    plazaCity = scrapy.Field()
    plazaName = scrapy.Field()
    plazaUrl = scrapy.Field()
    isHasShop = scrapy.Field()

class YuLiao(scrapy.Item):
    keyWords = scrapy.Field()
    data = scrapy.Field()

class BaiduTranslate(scrapy.Item):
    zh = scrapy.Field()
    en = scrapy.Field()


class WandaLeyuan(scrapy.Item):
    username = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()
    jingse = scrapy.Field()
    quwei = scrapy.Field()
    xingjiabi = scrapy.Field()
    comment = scrapy.Field()

class JukuuTranslate(scrapy.Item):
    keyword = scrapy.Field()
    zh = scrapy.Field()
    en = scrapy.Field()
    ru = scrapy.Field()


class Baike(scrapy.Item):
    keyword = scrapy.Field()
    context = scrapy.Field()
    linkword = scrapy.Field()
    tags = scrapy.Field()
    html = scrapy.Field()
    ismany = scrapy.Field()
    url= scrapy.Field()