from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from xkcd_scraper.items import XkcdComicItem

class XkcdComicSpider(CrawlSpider):
    name = 'xkcd-comics'
    start_urls = ['http://xkcd.com/1']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths='//a[@rel="next"]'),
             follow=True,
             callback='parse_comic'),
    )

    def parse_comic(self, response):
        hxs = HtmlXPathSelector(response)
        image = hxs.select('//div[@id="comic"]/img')

        item = XkcdComicItem()
        item['image_url'] = image.select('@src').extract()
        item['alt_text'] = image.select('@title').extract()
        item['transcript'] = hxs.select('//div[@id="transcript"]/text()').extract()

        return item
