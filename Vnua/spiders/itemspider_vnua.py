import scrapy
import json
import re
import dateparser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class ItemspiderHustSpider(scrapy.Spider):
    name = "itemspider_vnua"
    allowed_domains = ['vnua.edu.vn']
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ItemspiderHustSpider, self).__init__(*args, **kwargs)
        with open('linkitem.json', 'r') as f:
            data = json.load(f)
            self.start_urls = [item['link'] for item in data][:50]

    def parse(self, response):
        title = response.css('h1.post-title::text').get()
        title = re.sub(r'[\\"]|‘', '', title).strip()

        datetime_str = response.css('span[class="h5"]::text').get()
        datetime_obj = dateparser.parse(datetime_str, languages=['vi'])

        content = response.css('div.post-content p::text::text').getall()
        cleaned_content = [text.strip() for text in content if text.strip()]
        cleaned_content = ' '.join(cleaned_content)
        cleaned_content = re.sub(r'[\\"]|‘', '', cleaned_content).strip()
        image_url = response.css('img.img-auto::attr(scr)').extract_first()
        if image_url == None:
          image_url = response.css('img.imgtelerik::attr(scr)').extract_first()
        if image_url.startswith('/uploads'):
            image_url = "https://www.vnua.edu.vn" + image_url
        news_url = response.url
        yield {
            'title': title,
            'date': datetime_obj,
            'content': cleaned_content,
            'image_url': image_url,
            'news_url': news_url,
            'publication' : "vnua",
        }