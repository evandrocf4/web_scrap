import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


pastas = ['2025-05', '2025-04', '2025-03', '2025-02', '2025-01', '2024-12', '2024-11', '2024-10', '2024-09',
          '2024-08', '2024-07', '2024-06', '2024-05', '2024-04', '2024-03', '2024-02', '2024-01', '2023-12',
          '2023-11', '2023-10', '2023-09', '2023-08', '2023-07', '2023-06', '2023-05']

URL_BASE = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
PASTA_DESTINO = "dados_cnpj"

# Cria a pasta de destino se não existir
os.makedirs(PASTA_DESTINO, exist_ok=True)

for pasta in pastas:
    url = f"{URL_BASE}{pasta}/"
    print(f"\n🔍 Acessando: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        continue

    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra todos os links para arquivos .zip
    zip_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

    print(f"📁 {len(zip_links)} arquivos .zip encontrados em {pasta}.")

    # Faz o download de cada arquivo
    for link in tqdm(zip_links, desc=f"⬇️ Baixando arquivos de {pasta}"):
        nome_arquivo = os.path.basename(link)
        os.makedirs(f"{PASTA_DESTINO}/{pasta}", exist_ok=True)
        caminho_arquivo = os.path.join(f"{PASTA_DESTINO}/{pasta}", nome_arquivo)

        # Verifica se o arquivo já foi baixado
        if os.path.exists(caminho_arquivo):
            continue

        url_download = f"{url}{link}"
        try:
            with requests.get(url_download, stream=True) as r:
                r.raise_for_status()
                with open(caminho_arquivo, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except requests.RequestException as e:
            print(f"❌ Erro ao baixar {url_download}: {e}")
            continue

print("\n✅ Download concluído.")
