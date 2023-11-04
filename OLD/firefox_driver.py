from selenium  import webdriver
from selenium.webdriver.firefox.options import Options

def liga_firefox(url,visual_live):
    #visual_live: True, False
    option = Options()
    option.headless = visual_live
    driver = webdriver.Firefox(options=option)
    driver.get(url)

    return driver



def desliga_firefox(driver_instanciado):


    return driver_instanciado.quit()