from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from DLWebComics.items import WebComicItem
from urlparse import urljoin

class XkcdComicSpider(CrawlSpider):
    name = "xkcd"
    start_id = 1
    start_urls = ['http://xkcd.com/' + str(start_id)]
    rules = (Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'),
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
        title = sel.xpath('//div[@id="ctitle"]/text()').extract()
        alt_text = image.xpath('@title').extract()
        if len(src) > 0 and len(title) > 0 and len(alt_text) > 0:
            item = WebComicItem()
            # Set attributes
            item['image_url'] = urljoin("http://", src[0])
            item['image_num'] = str(self.start_id)
            item['title'] = title[0]
            item['alt_text'] = alt_text[0]
            item['transcript'] = sel.xpath('//div[@id="transcript"]/text()').extract()[0]
            item['ext'] = src[0].split('.')[-1]
            self.start_id += 1
            return item
        else:
            self.start_id += 1
            return []
