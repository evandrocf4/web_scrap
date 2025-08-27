# Databricks notebook source
import os
from pathlib import Path
from tqdm import tqdm

CAMINHO_ORIGEM = "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/landing"
CAMINHO_DESTINO = "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/raw"

# Lista os diretórios do caminho de origem
pastas = [p for p in dbutils.fs.ls(CAMINHO_ORIGEM) if p.isDir()]

for pasta in tqdm(pastas, desc="📁 Processando diretórios"):
    nome_pasta = os.path.basename(pasta.path.rstrip("/"))
    arquivos = dbutils.fs.ls(pasta.path)

    for arquivo in tqdm(arquivos, desc=f"📄 {nome_pasta}", leave=False):
        if arquivo.isDir():
            continue

        nome_original = os.path.basename(arquivo.name)
        nome_base = nome_original

        # 1. Se termina com 'CSV' sem ponto
        if nome_original.endswith("CSV") and not nome_original.endswith(".CSV"):
            nome_base = nome_original[:-3] + ".CSV"

        # 2. Se não termina com .CSV
        elif not nome_original.upper().endswith(".CSV"):
            nome_base = nome_original + ".CSV"

        # 3. Insere o nome do diretório antes do .CSV
        nome_final = nome_base.replace(".CSV", f"_{nome_pasta}.CSV")

        # Caminho de destino final (tudo no mesmo diretório)
        caminho_origem = arquivo.path
        caminho_destino = f"{CAMINHO_DESTINO}/{nome_final}"

        # Copia com renomeação
        try:
            dbutils.fs.cp(caminho_origem, caminho_destino)
        except Exception as e:
            print(f"❌ Erro ao copiar {caminho_origem} ➝ {caminho_destino}: {e}")

print("\n✅ Todos os arquivos foram renomeados e copiados para o diretório único 'raw/raw'.")
