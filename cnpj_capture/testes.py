import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

# URL base do site da Receita Federal
BASE_URL = 'https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/'

# Diretório onde os arquivos serão salvos
DOWNLOAD_DIR = 'dados_cnpj'

def get_links(url):
    """Obtém todos os links da página fornecida."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href != '../':
            links.append(href)
    return links

def download_file(url, dest_path):
    """Faz o download de um arquivo com barra de progresso."""
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=dest_path,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def main():
    # Certifica-se de que o diretório de download existe
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Obtém os subdiretórios (normalmente por ano ou categoria)
    subdirs = get_links(BASE_URL)

    for subdir in subdirs:
        subdir_url = urljoin(BASE_URL, subdir)
        subdir_path = os.path.join(DOWNLOAD_DIR, subdir.strip('/'))
        os.makedirs(subdir_path, exist_ok=True)

        # Obtém os arquivos ZIP dentro do subdiretório
        files = get_links(subdir_url)
        for file in files:
            if file.endswith('.zip'):
                file_url = urljoin(subdir_url, file)
                dest_file = os.path.join(subdir_path, file)
                if not os.path.exists(dest_file):
                    print(f'Baixando {file_url} para {dest_file}')
                    download_file(file_url, dest_file)
                else:
                    print(f'Arquivo {dest_file} já existe. Pulando download.')

if __name__ == '__main__':
    main()
    print('terminei')
