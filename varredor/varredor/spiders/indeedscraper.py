import scrapy


class IndeedSpider(scrapy.Spider):
    name = 'vagasbot'

    def start_requests(self):
        urls = [
            'https://br.indeed.com/jobs?q=Python&l=&from=searchOnHP&vjk=6bd88114d2731350']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for vagas in response.xpath('//td[@class="resultContent css-1qwrrf0 eu4oa1w0"]'):
            yield {
                'Cargo': vagas.xpath('.//span[1]/text()').get(),
                'Empresa': vagas.xpath('.//div//div[1]/span/text()').get(),
                'Local': vagas.xpath('.//div//div[2]/span/text()').get(),
                'Link': 'https://br.indeed.com' + vagas.xpath('.//div//h2//a/@href').get()
            }

        try:
            link_next_page = response.xpath(
                '//a[@data-testid="pagination-page-next"]/@href').get()

            if link_next_page is not None:
                next_page = 'https://br.indeed.com' + link_next_page
                yield scrapy.Request(url=next_page, callback=self.parse)

        except Exception as error:
            print('Chegamos na última página')
