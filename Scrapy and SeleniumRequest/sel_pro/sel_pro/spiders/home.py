#Author: Md.Fazlul Hoque
#Source: Stackoverflow and answered by the author
#Source link: https://stackoverflow.com/questions/70252583/spider-closes-without-error-messages-and-does-not-scrape-all-the-pages-in-the-pa/70253486#70253486


import scrapy
from scrapy_selenium import SeleniumRequest


class HomesSpider(scrapy.Spider):
    name = 'homes'
    def remove_characters(self, value):
        return value.strip(' m²')

    def start_requests(self):
        urls=[f'https://www.vivanuncios.com.mx/s-venta-inmuebles/queretaro/page-{i}/v1c1097l1021p50'.format(i) for i in range(1,51)]
        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=5,
                callback=self.parse
                )

    def parse(self, response):
        homes = response.xpath("//div[@id='tileRedesign']/div")
        for home in homes:
            yield {
                'price': home.xpath("normalize-space(.//span[@class='ad-price']/text())").get(),
                'location': home.xpath(".//div[@class='tile-location one-liner']/b/text()").get(),
                'description': home.xpath(".//div[@class='tile-desc one-liner']/a/text()").get(),
                'bathrooms': home.xpath("//div[@class='chiplets-inline-block re-bathroom']/text()").get(),
                'bedrooms': home.xpath(".//div[@class='chiplets-inline-block re-bedroom']/text()").get(),
                'm2': self.remove_characters(home.xpath("normalize-space(.//div[@class='chiplets-inline-block surface-area']/text())").get()),
                'link': home.xpath("//div[@class='tile-desc one-liner']/a/@href").get()
            }
