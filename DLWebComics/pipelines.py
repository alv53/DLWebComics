# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def sanitizeFileName(raw):
    # This is what I get for including alt text in the title
    return "".join(x for x in raw if x.isalnum()
                                     or x == ' '
                                     or x == '('
                                     or x == ')')

class WebComicImagesPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')
    spider = None

    def process_item(self, item, spider):
        self.spider = spider
        return ImagesPipeline.process_item(self, item, spider)

    def get_images(self, response, request, info):
        for key, image, buf, in super(WebComicImagesPipeline,
                                      self).get_images(response,
                                                       request,
                                                       info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_nums': item["image_nums"],
                                 'title': item["title"],
                                 'alt_text': item["alt_text"]})
                for x in item.get('image_urls', [])]

    def change_filename(self, key, response):
        # sanitize file name
        cleanNum = sanitizeFileName(response.meta['image_nums'][0])
        cleanTitle = sanitizeFileName(response.meta['title'][0])
        cleanAltText = sanitizeFileName(response.meta['alt_text'][0])

        name = self.spider.name + '/' + ""
        if cleanNum != "":
            name += cleanNum
        if cleanTitle != "":
            name += " - " + cleanTitle
        if cleanAltText != "":
            name += " - " + cleanAltText
        name += ".jpg"
        return name
