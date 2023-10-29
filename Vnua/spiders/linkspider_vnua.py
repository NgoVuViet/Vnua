import scrapy

class LinkspiderVnuaSpider(scrapy.Spider):
    name = "linkspider_vnua"
    allowed_domains = ["vnua.edu.vn"]
    start_urls = ["https://vnua.edu.vn/tin-tuc-su-kien"]
    visited_urls = set()

    def parse(self, response):
        links = response.css('.box-cate a::attr(href)').getall()  # Removed the extra dot in 'div[class=".box-cate"]'
        for link in links:
            if link in self.visited_urls:
                continue  # Skip already visited links
            self.visited_urls.add(link)
            yield {
                'link': link
            }
