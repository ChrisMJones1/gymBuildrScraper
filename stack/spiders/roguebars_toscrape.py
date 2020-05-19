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
            stackitem['_id'] = item.xpath("@data-item-sku").extract()

            stackitem['productName'] = item.xpath(".//h2/a/text()").extract_first()
            stackitem['price'] = item.xpath('.//span[@class="price"]/text()').extract_first()
            stackitem['imageUrl'] = item.xpath('.//img/@src').extract_first()
            yield scrapy.Request(item.xpath('.//a[@class="product-image"]/@href').extract_first(), callback=self.parse_item, meta={'stackitem': stackitem})
        next_page_url = response.xpath(".//a[@class='next']/@href").extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_item(self, response):
        stackitem = response.meta['stackitem']
        stackitem['description'] = response.xpath('.//div[@class="block_content"]/p/text()').extract()
        stackitem['rating'] = response.xpath('.//span[@itemprop="ratingValue"]/text()').extract_first()
        stackitem['categories'] = response.xpath('.//li[contains(@class, "category")]/a/text()').extract()
        return stackitem