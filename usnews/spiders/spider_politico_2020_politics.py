# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
            
import scrapy
from scrapy.crawler import CrawlerProcess
import xml.etree.ElementTree

class SpiderPolitico2020Politics(scrapy.Spider):
    name = "SpiderPolitico2020Politics"
    
    def start_requests(self):
        pages = list(range(1, 241))
        for page in pages:
            urls = ['https://www.politico.com/politics/' + str(page)]
            for url in urls:
                yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        links = response.css('h3 > a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(url = link, callback = self.parse_article)
          
    def parse_article(self, response):
        title = response.css('h2.headline::text').get()
        description = response.xpath('//meta[@property="og:description"]/@content').get()
        author = response.css('p.story-meta__authors > span > a::text').get()
        if author is None:
            author = response.css('p.story-meta__authors > span::text').get()
        content = response.css('p.story-text__paragraph::text').extract()
        content = [s.strip() for s in content]
        content = ' '.join(map(str, content))
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        date = response.css('p.story-meta__timestamp > time::text').get()
        category = response.css('p.category > a::text').get()
        yield {'Title': title,
               'Description': description,
               'Content': content,
               'URL': url,
               'Date': date,
               'Author' : author,
               'Category': category}   
