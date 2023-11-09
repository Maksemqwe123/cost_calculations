import scrapy


class FirmsSpider(scrapy.Spider):
    name = "firms_spider"
    allowed_domains = ["firmsdata.ru"]
    start_urls = ["https://firmsdata.ru/gomel/"]

    def parse(self, response):
        end_url = response.xpath("//li[@class='page-item']/a/@href").extract()[1].split('/')[-2]

        for link in response.xpath("//div[@style='margin-bottom: 15px; border-bottom: 1px solid #ccc']/div/a[@title!='Позвонить']/@href").extract():
            yield response.follow(link, callback=self.firms_parse)

        for link in range(1, int(end_url) + 1):
            yield response.follow(f'https://firmsdata.ru/gomel/{link}/', callback=self.parse)

    def firms_parse(self, response):
        name_firm = response.xpath("//h1/text()").extract()[0]
        street_name = response.css("div.bs-callout.bs-callout-info::text").extract_first()
        street_name = street_name.split('по адресу ')[1].split(' в городе')[0]
        category = response.xpath("//p/a/text()").extract()[0]

        firms_data_dict = {
            'name_firm': name_firm,
            'street_name': street_name,
            'category': category
        }
        yield firms_data_dict
