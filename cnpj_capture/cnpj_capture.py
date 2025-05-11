import os
import requests
from bs4 import BeautifulSoup

def get_months_and_years(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    months_and_years = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if '/dados/' in href and '-' in href:  # Verifique se o link aponta para um diretório de dados e contém um "-" (indicador de mês e ano)
            months_and_years.append(href.split('/')[-1])
    
    return months_and_years

def download_files(url, save_dir):
    # Obter todos os meses e anos
    months_and_years = get_months_and_years(url)

    for month_and_year in months_and_years:
        print(f"Downloading files from {month_and_year}")
        download_files_from_directory(f"{url}/{month_and_year}", save_dir)

def download_files_from_directory(url, save_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/dados/' in href:  # Verifique se o link aponta para um diretório de dados
            links.append(href)
    
    # Download dos arquivos
    for link in links:
        file_url = f"https://arquivos.receitafederal.gov.br{link}"  # Construir a URL completa
        file_name = os.path.basename(file_url)  # Obter o nome do arquivo
        
        print(f"Downloading {file_name}")
        response = requests.get(file_url, stream=True)
        
        with open(os.path.join('../data', file_name), 'wb') as f:  # Alterado para salvar os arquivos no diretório "data"
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    print('Downloads completed')

# Usar a função
download_files('https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj', '\\jerusalem\media_library\repositories\web_scrap\cnpj_capture\data')
