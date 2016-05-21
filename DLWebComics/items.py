# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WebComicItem(Item):
    image_urls = Field()
    image_nums= Field()
    title = Field()
    alt_text = Field()
    transcript = Field()
    ext = Field()
