import scrapy
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy1.items import Product




class EuroluxSpider(CrawlSpider):
    name = 'eurolux'
    allowed_domains = ['eurolux.de']
    start_urls = ['https://eurolux.de/']
    allow=('/category|/product',)
    deny=('pdf|/en/')
    currency = 'EUR'

    rules = (
        Rule(LinkExtractor(allow=allow,deny=deny), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        # Check if the URL contains "/product"
        if "/product" not in response.url:
            self.log(f'Skipping non-product page: {response.url}')
            return
        
        # parse the english versoin of the page
        # yield scrapy.Request(url='https://eurolux.de/en/product/', callback=self.parse_english_page)


        item = Product()

        item['title'] = response.css('.font-weight-bold.text-center::text').get()
        #item['description']  = bleach_html(response.css('.text-md-h6').get()) + bleach_html(response.css('.v-col-12 , strong , .font-weight-bold').get())
        item['sku'] = response.css(".text-secondary::text").get() or ""
        item.set_price (response.css('.v-col-12 .v-col .text-uppercase strong::text').get())
        item['price_currency'] = self.currency
        item['url'] = response.url

        yield item


    def parse_english_page(self, response):
        # parse the english version of the page

        title = response.css('.font-weight-bold.text-center::text').get()
        description  = response.css('.text-md-h6').get() + response.css('.v-col-12 , strong , .font-weight-bold').get()

        return {
            'title': title,
            'description': description,
        }



