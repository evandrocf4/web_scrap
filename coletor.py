import time
import pandas as pd
from firefox_driver import liga_firefox, desliga_firefox
from selenium  import webdriver #importa para o firefox_drive funcionar aqui temporariamente
from selenium.webdriver.firefox.options import Options #importa para o firefox_drive funcionar aqui temporariamente
#from selenium.webdriver.firefox import Options #importa para o firefox_drive funcionar aqui temporariamente
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.service import Service

#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

def main():


# 1. Pegar conteúdo HTML a partir da URL
    url_statusinvest = 'https://statusinvest.com.br/acoes/vale3'
    
    
    service = Service(executable_path=r"E:\Program Files\geckodriver-v0.32.2-win64")
    driver = webdriver.Firefox(service=service)
    driver.get(url_statusinvest)
    sleep(5)
    # colocar o executable
    table_rows = driver.find_element(By.XPATH, '(//table)[1]//tr')
    parsed_table = []
    for row in table_rows:
        row_data = {
            'tipo': row.xpath('.//td[1]//text()').get(''),
            'data_com': row.xpath('.//td[1]//text()').get(''),
            'pagamento': row.xpath('.//td[1]//text()').get(''),
            'valor': row.xpath('.//td[1]//text()').get(''), 
        }
        parsed_table.append(row_data)
    
    print(parsed_table)






if __name__ == "__main__":
    main()


'''
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://selenium.dev/')

'''