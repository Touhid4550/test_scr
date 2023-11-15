import scrapy
from urllib.parse import urlsplit
import json
import requests
import xml.etree.ElementTree as ET

class FoethSpider(scrapy.Spider):
    name = "foeth_spider"
    allowed_domains = ["foeth.com"]
    # start_urls = ['https://www.foeth.com/en/mixers/universal-mixers/collette-gral-600-universal-mixer-062a304']
    serial_no=0
    def start_requests(self):
        url = "https://www.foeth.com/pub/sitemap/en/sitemap.xml"
        response = requests.get(url)
        with open('sitemap.xml', 'wb') as file:
            file.write(response.content)
        
        sitemap_file = 'sitemap.xml'

        urls =  self.get_loc_from_sitemap(sitemap_file)
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.serial_no+=1
        title = self.get_text(response, '//span[@data-ui-id="page-title-wrapper"]/text()')
        categories = ""
        cat_dict = {}
        cat_keys = ["Cat 1", "Cat 2", "Cat 3"]
        cat_values = self.get_texts(response, '//div[@class="breadcrumbs"]//a/span/text()')
        cat_dict = dict(zip(cat_keys, cat_values))
        categories = json.dumps(cat_dict)

        manufacturer = self.get_text(response, '//li[@data-attr="g_make"]/span[2]/a/text()')
        sku = self.get_text(response, '//li[@data-attr="sku"]/span[2]/text()')

        images = "\n".join(self.get_attributes(response, '//div[@class="gallery-thumbs"]/figure/img', 'data-full'))

        details = ""
        details_lis = response.xpath('//div[@class="product-info-main-wrapper-fixed"]//li')
        for details_li in details_lis:
            details_title = self.get_text(details_li, './text()')
            details_data = " ".join(self.get_texts(details_li, './span/text()'))
            details += f"{details_title} {details_data}\n"

        year = self.get_text(response, '//li[@data-attr="g_new"]/span[2]/text()')
        category = self.get_text(response, '//span[@class="sub-base"]/text()')
        model = self.get_text(response, '//li[@data-attr="g_type"]/span[2]/text()')

        supplier = urlsplit(response.url).netloc

        yield {
            "SL": self.serial_no,
            "URL": response.url,
            "Title": title,
            "SKU": sku,
            "Manufacturer": manufacturer,
            "Model": model,
            "Year": year,
            "Category": category,
            "Categories": categories,
            "Supplier": supplier,
            "Images": images,
            "Details": details
        }

    def get_loc_from_sitemap(self, sitemap_file):

        tree = ET.parse(sitemap_file)
        # count=1
        url_list=[]
        # Find all the <url> tags
        for url in tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            # Find the <priority> tag
            priority = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
            # print(priority)
            # Check if the priority is 1.0
            if priority.text == '1.0':
                # Find the <loc> tag and print its text
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                # print(count)
                loc_url=loc.text
                url_list.append(loc_url)
        return url_list
            # yield url

    def get_text(self, response, xpath):
        value = response.xpath(xpath).get()
        return value.strip() if value else ""

    def get_texts(self, response, xpath):
        return [text.strip() for text in response.xpath(xpath).getall()]

    def get_attributes(self, response, xpath, attribute):
        return response.xpath(f'{xpath}/@{attribute}').getall()

