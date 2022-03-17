
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

def remove_currency(value):
    return value.replace('Rs','').strip()

def filter_price(value):
    if value.isdigit():
        return value

class OlxItem(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_currency)
    )