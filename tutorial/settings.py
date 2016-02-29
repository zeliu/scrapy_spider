# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

ITEM_PIPELINES = {
    'tutorial.pipelines.TutorialPipeline': 300,
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1
}

IMAGES_STORE = 'image'
IMAGES_EXPIRES = 90

#反ban策略一：禁用COOKIES
COOKIES_ENABLED = False

#取消默认的useragent,使用新的useragent,反ban策略二
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'tutorial.spiders.rotate_useragent.RotateUserAgentMiddleware': 400
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
