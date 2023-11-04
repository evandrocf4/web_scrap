# -*- coding: ISO-8859-1 -*-
import scrapy
import csv

class StatusInvestSpider(scrapy.Spider):
    name = "status_invest"
    start_urls = ["https://statusinvest.com.br/acoes/bbas3"]
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.custom_headers, callback=self.parse)

    def parse(self, response):
        table_data = []
        #print("AQUI 1")
        for page_number in range(1, 8):  # Número de páginas a serem percorridas
            table = response.xpath('//table')
            table_rows = response.xpath('(//table)[1]//tr')

            # Realize o processamento da tabela
            rows = table.xpath('.//tbody/tr')
            #for row in rows:
            for index, row in enumerate(table_rows):
                if index != 0:
                    tipo = row.xpath('.//td[1]/text()').get('')
                    data_com = row.xpath('.//td[2]/text()').get('')
                    pagamento = row.xpath('.//td[3]/text()').get('')
                    valor = row.xpath('.//td[4]/text()').get('')
                    table_data.append([tipo, data_com, pagamento, valor])
                else:
                    continue
                # if index == 0:
                #     continue
                print("AQUI 2")
            #print("AQUI")
            # Navegue para a próxima página
            next_page = response.xpath(f'//ul[@class="pagination mb-0"]/li[@data-page="{page_number + 1}"]/a')
            if next_page:
                next_page_url = next_page.xpath('@href').get()
                yield response.follow(next_page_url, headers=self.custom_headers, callback=self.parse)
            #print('\n\n\n', table_data,'\n\n\n')

        with open('data_raw.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Tipo', 'Data Com', 'Pagamento', 'Valor'])
            csv_writer.writerows(table_data)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(StatusInvestSpider)
    process.start()
