import scrapy

from .dataclass import Apartment


class OlxScrapy(scrapy.Spider):
    name = "OlxScrapy"

    def start_requests(self):
        url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723'
        yield scrapy.Request(url=url, callback=self.response_parser)

    def response_parser(self, response):
        url_prefix = "https://www.olx.in"
        for selector in response.xpath("//li[@class='_1DNjI']"):
            redirect_url = url_prefix + selector.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=redirect_url, callback=self.structure)
        next_page_link = response.css('link[rel="next"]::attr(href)').extract_first()
        print("next_page_link>>>>>>>>>>>>>>>>>>>>>>>>>", next_page_link)
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)

    def structure(self, response):
        a = Apartment()
        a['property_name'] = response.xpath("//span[@class='dBLgK']/text()").extract_first()
        a['property_id'] = response.xpath("//div[@class='_1-oS0']//strong/text()").extract()[2]
        a['breadcrumbs'] = response.xpath("//ol[@class='rui-2Pidb']/li/a[@class='_26_tZ']/text()").extract()
        a['price'] = response.xpath("//span[@class='T8y-z']/text()").extract_first()
        a['image_url'] = response.xpath("//img[@class='_1Iq92']/@src").extract_first()
        a['description'] = ' '.join(response.xpath("//div[@data-aut-id='itemDescriptionContent']/p/text()").extract())
        a['location'] = ''.join(response.xpath("//div[@class='rui-99hme gp-Oc']/div[@class='rui-oN78c']"
                                               "/div[@class='_3Uj8e']/span[@class='_1RkZP']/text()").extract())
        a['property_type'] = ''.join(response.xpath("//span[@data-aut-id='value_type']/text()").extract())
        a['bathrooms'] = ''.join(response.xpath("//span[@data-aut-id='value_bathrooms']/text()").extract())
        a['bedrooms'] = ''.join(response.xpath("//span[@data-aut-id='value_bathrooms']/text()").extract_first())

        yield a
