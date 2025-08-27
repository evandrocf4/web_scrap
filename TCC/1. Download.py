import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import shutil

# Lista de pastas que contêm os arquivos
pastas = ['2025-05', '2025-04', '2025-03', '2025-02', '2025-01', '2024-12', '2024-11', '2024-10', '2024-09',
          '2024-08', '2024-07', '2024-06', '2024-05', '2024-04', '2024-03', '2024-02', '2024-01', '2023-12',
          '2023-11', '2023-10', '2023-09', '2023-08', '2023-07', '2023-06', '2023-05']

URL_BASE = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
PASTA_LOCAL_TEMP = "/tmp/dados_cnpj"
PASTA_DESTINO_ABFSS = "abfss://landing@gen2especializacao.dfs.core.windows.net/dados_cnpj"

# Cria a pasta local temporária
os.makedirs(PASTA_LOCAL_TEMP, exist_ok=True)

for pasta in pastas:
    url = f"{URL_BASE}{pasta}/"
    print(f"\n🔍 Acessando: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    zip_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

    print(f"📁 {len(zip_links)} arquivos .zip encontrados em {pasta}.")

    # Pasta local temporária para essa subpasta
    pasta_local_sub = os.path.join(PASTA_LOCAL_TEMP, pasta)
    os.makedirs(pasta_local_sub, exist_ok=True)

    for link in tqdm(zip_links, desc=f"⬇️ Baixando arquivos de {pasta}"):
        nome_arquivo = os.path.basename(link)
        caminho_local = os.path.join(pasta_local_sub, nome_arquivo)

        if os.path.exists(caminho_local):
            continue

        url_download = f"{url}{link}"
        try:
            with requests.get(url_download, stream=True) as r:
                r.raise_for_status()
                with open(caminho_local, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except requests.RequestException as e:
            print(f"❌ Erro ao baixar {url_download}: {e}")
            continue

        # Caminho de destino no DBFS (montado sobre abfss via external location)
        caminho_dbfs_temp = f"/dbfs/mnt/landing_gen2_especializacao/dados_cnpj/{pasta}/{nome_arquivo}"

        # Cria pasta de destino se necessário
        os.makedirs(os.path.dirname(caminho_dbfs_temp), exist_ok=True)

        # Copia o arquivo do /tmp para /dbfs (que reflete o abfss)
        shutil.copy(caminho_local, caminho_dbfs_temp)

print("\n✅ Download concluído e arquivos movidos para o Data Lake.")