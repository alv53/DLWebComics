from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from DLWebComics.items import WebComicItem
from urlparse import urljoin

class XkcdComicSpider(CrawlSpider):
    name = 'xkcd'
    start_id = 1
    start_urls = ['http://xkcd.com/' + str(start_id)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'),
             follow=True,
             callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        if self.start_id == 404:
            self.start_id = 405
        sel = Selector(response=response)
        image = sel.xpath('//div[@id="comic"]/img')
        # One comic has image in a hyperlink
        if len(image.xpath('@src').extract()) == 0:
            image = sel.xpath('//div[@id="comic"]/a/img')
        src = image.xpath('@src').extract()
        if len(src) > 0:
            item = WebComicItem()
            url = src[0]
            # Set attributes
            item['image_urls'] = [urljoin("http://", url)]
            item['image_nums'] = [str(self.start_id)]
            item['title'] = sel.xpath('//div[@id="ctitle"]/text()').extract()
            item['alt_text'] = image.xpath('@title').extract()
            item['transcript'] = sel.xpath('//div[@id="transcript"]/text()').extract()
            self.start_id += 1
            return item
        else:
            self.start_id += 1
            return []

class SmbcComicSpider(CrawlSpider):
    name = "smbc"
    start_urls = ['http://www.smbc-comics.com/index.php?id=1']

    rules = (
                Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'),
                     follow=True,
                     callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        sel = Selector(response=response)
        image = sel.xpath('//div[@id="comicbody"]/a/img')
        src = image.xpath('@src').extract()
        if len(src) > 0:
            item = WebComicItem()
            url = src[0]
            num = response.url.split('=')[1]
            # Set attributes
            item['image_urls'] = [urljoin("http://www.smbc-comics.com",
                                          url)]
            item['image_nums'] = [str(num)]
            item['title'] = [""]
            item['alt_text'] = [""]
            item['transcript'] = [""]
            return item
        else:
            return []
