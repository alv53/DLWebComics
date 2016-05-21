from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from DLWebComics.items import WebComicItem
from urlparse import urljoin

class SmbcComicSpider(CrawlSpider):
    name = "smbc"
    start_urls = ['http://www.smbc-comics.com/index.php?id=1']

    rules = (Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'),
             follow=True,
             callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        sel = Selector(response=response)
        image = sel.xpath('//div[@id="comicbody"]/a/img')
        src = image.xpath('@src').extract()
        if len(src) > 0:
            item = WebComicItem()
            num = response.url.split('=')[1]
            # Set attributes
            item['image_url'] = urljoin("http://www.smbc-comics.com", src[0])
            item['image_num'] = str(num)
            item['title'] = ""
            item['alt_text'] = ""
            item['transcript'] = ""
            item['ext'] = src[0].split('.')[-1]
            return item
        else:
            return []
