# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.crawler import CrawlerProcess
from usnews.items import usnewsItem

class SpiderAxiosItem(scrapy.Spider):
    name = "SpiderAxiosItem"
    
    def start_requests(self):
        urls = ['https://www.axios.com/']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        articles =  response.css('h6.sc-31t5q3-6')
        for article in articles:
            item = usnewsItem()
            item['titles'] = article.css('a.title-link::text ').get()
            item['links'] = article.css('a.title-link::attr("href")').get()
            yield item