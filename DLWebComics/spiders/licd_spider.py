from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from DLWebComics.items import WebComicItem
from urlparse import urljoin

class LicdComicSpider(CrawlSpider):
    name = "licd"
    start_urls = ['http://www.leasticoulddo.com/comic/20030210/']

    rules = (Rule(LinkExtractor(restrict_xpaths='//a[@id="nav-large-next"]'),
             follow=True,
             callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        sel = Selector(response=response)
        image = sel.xpath('//div[@id="comic-img"]/a/img')
        src = image.xpath('@src').extract()
        if len(src) > 0:
            item = WebComicItem()
            num = str(response.url.split('/')[-2])
            if num == "auto-draft-2":
                num = "20130720"
            if len(num) > 8:
                num = num[:8]
            # Set attributes
            item['image_url'] = src[0]
            item['image_num'] = str(num)
            item['title'] = ""
            item['alt_text'] = ""
            item['transcript'] = ""
            item['ext'] = src[0].split('.')[-1]
            return item
        else:
            return []
