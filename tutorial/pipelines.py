# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from tutorial.items import MyJsonEncoder
class TutorialPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')
        self.file = codecs.open('test_data_utf8.json', 'wb', encoding='utf-8')
    #def process_item(self, item, spider):
    #    line = json.dumps(dict(item),cls=MyJsonEncoder) + "\n"
    #    self.file.write(line.decode('unicode_escape'))
    #    return item
    def process_item(self, item, spider):
        line=item['keyword']+'\001'+item['ismany']+'\001'+item['url']+'\001'+item['context']+'\001'+item['linkword']+'\001'+item['tags']+'\001'+item['html']+"\n"
        self.file.write(line)
        return item
    #def process_item(self, item, spider):
    #    return item
