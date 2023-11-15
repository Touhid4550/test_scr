# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
import bleach

def bleach_html(html_string):
        # Set html_string to an empty string if it is None
        html_string = html_string or ''

        # Define a set of allowed tags
        allowed_tags = ['br', 'p']

        # Use bleach to sanitize HTML content
        cleaned_html = bleach.clean(html_string, tags=allowed_tags, strip=True)

        # Replace tags with newline characters
        for tag in allowed_tags:
            cleaned_html = cleaned_html.replace(f'<{tag}>', '\n').replace(f'</{tag}>', '')

        return cleaned_html.strip()

class Product(scrapy.Item):
    sku= scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field() # e.g. EUR, USD
    price_type = scrapy.Field() # e.g. ON_REQUEST, FIXED
    location = scrapy.Field()
    
    url = scrapy.Field()

    def get_price(self):
        # Getter function
        return self['price']
    
    def set_price(self, value):
        # Custom setter function to remove spaces from the price
        if value is not None:
            self['price'] = bleach_html(value).replace("€","").replace(",","").replace(" ","").strip()
            
            
            test add