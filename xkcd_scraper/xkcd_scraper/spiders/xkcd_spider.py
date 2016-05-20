from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from xkcd_scraper.items import XkcdComicItem
from urlparse import urljoin

import os

class XkcdComicSpider(CrawlSpider):
    name = 'xkcd-comics'
    start_id = 1
    start_urls = ['http://xkcd.com/' + str(start_id)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'),
             follow=True,
             callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        sel = Selector(response=response)
        image = sel.xpath('//div[@id="comic"]/img')

        item = XkcdComicItem()
        if self.start_id == 404:
            self.start_id = 405
        if len(image.xpath('@src').extract()) == 0:
            image = sel.xpath('//div[@id="comic"]/a/img')
        print "len: " + str(len(image.xpath('@src').extract()))
        if len(image.xpath('@src').extract()) > 0:
            print "inside"
            url = image.xpath('@src').extract()[0]
            item['image_urls'] = [urljoin("http://", url)]
            item['image_names'] = [str(self.start_id)]
            item['alt_text'] = image.xpath('@title').extract()
            item['transcript'] =sel.xpath('//div[@id="transcript"]/text()') .extract()

            self.start_id += 1
            return item
        else:
            self.start_id += 1
            return []
