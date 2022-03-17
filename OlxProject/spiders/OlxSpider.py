import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from OlxProject.items import OlxItem

class OlxSpider(scrapy.Spider):
    name="OlxSpider"
    start_urls = [
        "https://www.olx.com.pk/punjab_g2003006/q-bicycle",
        # "https://www.olx.com.pk/sindh_g2003007/q-bicycle",
        # "https://www.olx.com.pk/balochistan_g2003001/q-bicycle",
        # "https://www.olx.com.pk/khyber-pakhtunkhwa_g2003005/q-bicycle",
        # "https://www.olx.com.pk/islamabad-capital-territory_g2003003/q-bicycle"
    ]

    def parse(self, response, **kwargs):
        for item in response.css('li[aria-label="Listing"]'):
            il = CustomLoader(item=OlxItem(), selector=item)

            il.add_xpath('title', "article/div[2]/a/@title")
            il.add_value('location', item.xpath('article/div[2]/div[2]/div/span/text()').get())
            il.add_xpath('date', 'article/div[2]/div[2]/div/span[2]/span/text()')
            il.add_xpath('image', 'article//picture/img/@data-src'),
            il.add_value('price', item.xpath('article/div[2]/div[1]/div[2]/span/text()').get())
            yield il.load_item()

        next_link = response.xpath('//button/span[.="Load more"]/parent::button/parent::a/@href').get()
        if next_link is not  None:
            yield response.follow(next_link, callback=self.parse)

class CustomLoader(ItemLoader):
    default_output_processor = TakeFirst()