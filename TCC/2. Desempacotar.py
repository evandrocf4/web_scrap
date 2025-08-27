import os
import zipfile
from pathlib import Path
from tqdm import tqdm
import shutil

# Caminhos base
CAMINHO_ABFSS_ORIGEM = "abfss://landing@gen2especializacao.dfs.core.windows.net/landing"
CAMINHO_ABFSS_DESTINO = "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/landing"
PASTA_LOCAL_TMP = "/tmp/landing_tmp"

# Lista todos os diretórios e arquivos zip em dados_cnpj
pastas = dbutils.fs.ls(CAMINHO_ABFSS_ORIGEM)

for pasta in pastas:
    if not pasta.isDir():
        continue
    
    nome_pasta = os.path.basename(pasta.path.rstrip("/"))
    arquivos_zip = dbutils.fs.ls(pasta.path)

    for arquivo in tqdm(arquivos_zip, desc=f"📦 Processando {nome_pasta}"):
        if not arquivo.name.endswith(".zip"):
            continue

        nome_arquivo = arquivo.name
        caminho_zip_abfss = arquivo.path
        caminho_zip_tmp = os.path.join(PASTA_LOCAL_TMP, nome_pasta, nome_arquivo)

        # Cria diretório local temporário
        os.makedirs(os.path.dirname(caminho_zip_tmp), exist_ok=True)

        # Copia do ABFSS para /tmp local
        dbutils.fs.cp(caminho_zip_abfss, f"file:{caminho_zip_tmp}")

        # Extrai conteúdo do .zip
        try:
            with zipfile.ZipFile(caminho_zip_tmp, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(PASTA_LOCAL_TMP, nome_pasta, "unzipped"))
        except Exception as e:
            print(f"❌ Erro ao descompactar {caminho_zip_tmp}: {e}")
            continue

        # Envia arquivos descompactados para o Data Lake
        pasta_unzip = Path(PASTA_LOCAL_TMP) / nome_pasta / "unzipped"
        for raiz, _, arquivos in os.walk(pasta_unzip):
            for nome in arquivos:
                caminho_local = os.path.join(raiz, nome)
                caminho_relativo = os.path.relpath(caminho_local, pasta_unzip)
                caminho_abfss_destino = f"{CAMINHO_ABFSS_DESTINO}/{nome_pasta}/{caminho_relativo}"

                try:
                    dbutils.fs.cp(f"file:{caminho_local}", caminho_abfss_destino)
                except Exception as e:
                    print(f"❌ Erro ao copiar {caminho_local} para {caminho_abfss_destino}: {e}")

        # Limpa arquivos temporários
        shutil.rmtree(os.path.join(PASTA_LOCAL_TMP, nome_pasta), ignore_errors=True)

print("\n✅ Todos os arquivos foram descompactados e copiados para o diretório raw.")
