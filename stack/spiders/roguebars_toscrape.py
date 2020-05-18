# -*- coding: utf-8 -*-
import scrapy

from stack.items import StackItem


class RoguebarsToscrapeSpider(scrapy.Spider):
    name = 'roguebars-toscrape'
    allowed_domains = ['roguecanada.ca']
    start_urls = ['http://roguecanada.ca/weightlifting-bars-plates']

    def parse(self, response):
        stackitem = StackItem()
        for item in response.css("li.item"):
            yield {
                '_id': item.xpath("@data-item-sku").extract(),
                'productName': item.xpath(".//h2/a/text()").extract_first(),
                'price': item.xpath('.//span[@class="price"]/text()').extract_first(),
                'imageUrl': item.xpath('.//img/@src').extract_first()
            }
            item_url = response.xpath('.//')
        next_page_url = response.xpath(".//a[@class='next']/@href").extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))