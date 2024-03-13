# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class pd_base(scrapy.Item):
    brand = scrapy.Field()
    product = scrapy.Field()
    pd_picture = scrapy.Field()
    dscnt_price = scrapy.Field()
    pd_strike = scrapy.Field()
    pd_dscnt_price = scrapy.Field()
    product_title = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    rating_count = scrapy.Field()
    pd_material = scrapy.Field()
    item_spec = scrapy.Field()
    comments = scrapy.Field()
    image_urls = scrapy.Field()
    product_id = scrapy.Field()
    seller_name = scrapy.Field()
    product_desc = scrapy.Field()
    sizes  = scrapy.Field()

