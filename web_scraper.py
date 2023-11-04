# -*- coding: ISO-8859-1 -*-
import scrapy
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        driver = webdriver.Chrome()
        driver.get(response.url)

        try:
            table_data = []

            while True:
                # Espera até que a tabela seja carregada
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//table'))
                )

                table = driver.find_element(By.XPATH, '//table')
                table_rows = table.find_elements(By.XPATH, './/tr')

                for index, row in enumerate(table_rows):
                    if index != 0:
                        tipo = row.find_element(By.XPATH, './/td[1]').text
                        data_com = row.find_element(By.XPATH, './/td[2]').text
                        pagamento = row.find_element(By.XPATH, './/td[3]').text
                        valor = row.find_element(By.XPATH, './/td[4]').text
                        table_data.append([tipo, data_com, pagamento, valor])

                # Verifica se há um próximo botão de página
                next_page = driver.find_elements(By.XPATH, '//li[@data-page]')
                if len(next_page) > 1:
                    next_page[1].click()
                else:
                    break

            with open('data_raw.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Tipo', 'Data Com', 'Pagamento', 'Valor'])
                csv_writer.writerows(table_data)

        finally:
            driver.quit()

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(StatusInvestSpider)
    process.start()
