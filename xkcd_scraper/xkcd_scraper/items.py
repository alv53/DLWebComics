# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class XkcdComicItem(Item):
    image_url = Field()
    alt_text = Field()
    transcript = Field()
