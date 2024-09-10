# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MonitorItem(scrapy.Item):
    Model = scrapy.Field()
    Price = scrapy.Field()
    Resolution = scrapy.Field()
    Manufacturer = scrapy.Field()
    ReviewStars = scrapy.Field()
