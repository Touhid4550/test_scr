import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Product


class KahCrawlSpider(CrawlSpider):
    name = "kah_crawl"
    allowed_domains = ["kahlschlichterle.de"]
    start_url = "https://www.kahlschlichterle.de/en/machines/"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url)

    urls_extractor = LinkExtractor(restrict_xpaths='//div[@class="col-md-3 col-sm-6"]/a')
    rules = (
        Rule(urls_extractor, callback="parse_item", follow=True)
    )

    def parse_item(self, response):
        item = Product()

        item['title'] = response.xpath('//h1/text()').get()
        sku = response.xpath('//div[strong[text()="SKU:"]]/text()').get()
        if sku: sku = sku.strip()
        item['sku'] = sku
        des_set = response.xpath('//div[@class="single-product-content"]/p[1]/text()').getall()
        description = []
        for text in des_set:
            description.append(text.strip())
        item['description'] = description
        rel_img_urls = response.xpath('//a[@data-fancybox="gallery"]/img/@src').getall()
        img_urls = []
        for rel_url in rel_img_urls:
            img_urls.append(f'https://www.kahlschlichterle.de/{rel_url}')
        item['img_urls'] = img_urls

        yield item

