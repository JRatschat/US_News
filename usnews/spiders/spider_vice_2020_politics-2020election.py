# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
            
import scrapy
from scrapy.crawler import CrawlerProcess
import xml.etree.ElementTree

def remove_tags(text): 
        return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

class SpiderVice2020Election(scrapy.Spider):
    name = "SpiderVice2020Election"
    
    def start_requests(self):
        pages = list(range(1, 22))
        for page in pages:
            urls = ['https://www.vice.com/en_us/topic/2020?page=' + str(page)]
            for url in urls:
                yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        links = response.css('h3.vice-card-hed > a::attr("href")').extract()
        for link in links:
            link = 'https://www.vice.com' + link
            yield scrapy.Request(url = link, callback = self.parse_article)
          
    def parse_article(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        description = response.xpath('//meta[@property="og:description"]/@content').get()
        author = response.css('div.contributor__meta > div > a::text').get()
        content = response.xpath('//span[@data-component="TextBlock"]/p/text()').extract()
        content = [s.strip() for s in content]
        content = ' '.join(map(str, content))
        url = response.xpath('//link[@rel="canonical"]/@href').get()
        date = response.xpath('//div[@class="article__header__datebar__date--original"]/text()').get()
        category = response.xpath('//meta[@name="keywords"]/@content').get()
        yield {'Title': title,
               'Description': description,
               'Content': content,
               'URL': url,
               'Date': date,
               'Author' : author,
               'Category': category}
   
     
