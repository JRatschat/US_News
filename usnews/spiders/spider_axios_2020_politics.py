# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
            
import scrapy
from scrapy.crawler import CrawlerProcess
import xml.etree.ElementTree

def remove_tags(text):
        return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

class SpiderAxios2020Politics(scrapy.Spider):
    name = "SpiderAxios2020Politics"
    
    def start_requests(self):
        days = list(range(1, 32))
        months = list(range(1, 9))
        for month in months:
            for day in days:
                urls = ['https://www.axios.com/politics-policy/2020/' + 
                        str(month)  + 
                        '/' + 
                        str(day)]
                for url in urls:
                    yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        links = response.css('a.title-link::attr("href")').extract()
        for link in links:
            yield scrapy.Request(url = link, callback = self.parse_article)
            
    def parse_article(self, response):
        title = response.css('h1.leading-tight::text').get()
        description = response.xpath('//meta[@name="description"]/@content').get()
        content = remove_tags(response.css('div.gtm-story-text').get())
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        date = response.xpath('//meta[@name="date"]/@content').get()
        author = response.xpath('//meta[@name="author"]/@content').get()
        category = response.xpath('//meta[@name="category"]/@content').get()
        yield {'Title': title, 
               'Description': description,
               'Content': content, 
               'URL': url, 
               'Date': date,
               'Author' : author,
               'Category' : category}