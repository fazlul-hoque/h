#Author: Md.Fazlul Hoque
#Source: Stackoverflow and answered by the author
#Source link: https://stackoverflow.com/questions/71560470/how-to-use-scrapy-and-selenium-to-get-data-from-a-website-which-uses-javascript/71561964#71561964


import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
#from selenium.common.exceptions import NoSuchElementException

class MeldingenSpider(scrapy.Spider):
    name = 'dingen'

    responses = []

    def start_requests(self):
        yield SeleniumRequest(
            url='http://ftp.112meldingen.nl/index.php',
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        intial_page = driver.page_source
        self.responses.append(intial_page)
        driver.implicitly_wait(2)

        for resp in self.responses:
            r = Selector(text=resp)
            articles = r.css('table#alerts')
            for article in articles:
            #if "haven" in article.css('div.title a::text').get():
                    yield {
                        'headline': article.css('td.bold a::text').get() ,
                        'timestamp': article.css('td.bold span::text').get().replace('\xa0\xa021',''),
                        'location' : [x.replace('\xa0',' ') for x in article.xpath('.//tr/td[@class="bold center"]/following-sibling::td//text()').getall()][-1]
           

         }