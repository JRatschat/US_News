# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
            
import scrapy
from scrapy.crawler import CrawlerProcess
import xml.etree.ElementTree

def remove_tags(text): 
        return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

class SpiderBreitbart2020Politics(scrapy.Spider):
    name = "SpiderBreitbart2020Politics"
    
    def start_requests(self):
        pages = list(range(1, 681))
        for page in pages:
            urls = ['https://www.breitbart.com/politics/page/' + 
                    str(page)  + 
                    '/']
            for url in urls:
                yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        links = response.css('article > a::attr("href")').extract()
        for link in links:
            link = 'https://www.breitbart.com' + link
            yield scrapy.Request(url = link, callback = self.parse_article)
          
    def parse_article(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath('//meta[@property="og:description"]/@content').get()
        author = response.xpath('//meta[@name="author"]/@content').get()
        content = response.css('div.entry-content p::text').extract()
        content = [s.strip() for s in content]
        content = ' '.join(map(str, content))
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        date = response.xpath('//meta[@property="article:published_time"]/@content').get()
        category = response.xpath('//meta[@property="article:categories"]/@content').get()
        yield {'Title': title,
               'Description': description,
               'Content': content,
               'URL': url,
               'Date': date,
               'Author' : author,
               'Category': category}
   
      
