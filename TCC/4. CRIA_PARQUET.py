from pyspark.sql import SparkSession
from tqdm import tqdm
import os

spark = SparkSession.builder.getOrCreate()

CAMINHO_ORIGEM = "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/raw"

# Mapeamento de substrings para diretórios de destino
mapeamento = {
    "CNAE": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/cnaes",
    "SIMPLES": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/simples",
    "MOTI": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/motivos",
    "MUNIC": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/municipios",
    "NATJU": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/naturezas",
    "PAIS": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/paises",
    "QUALS": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/qualificacoes",
    "EMPRE": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/empresas",
    "ESTABELE": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/estabelecimentos",
    "SOCIO": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/socios"
}

# Lista todos os arquivos .CSV no diretório de origem
arquivos = [f for f in dbutils.fs.ls(CAMINHO_ORIGEM) if f.path.upper().endswith(".CSV")]

print(f"🔍 {len(arquivos)} arquivos .CSV encontrados.")

for arquivo in tqdm(arquivos, desc="🚀 Processando arquivos"):
    nome_arquivo = os.path.basename(arquivo.path).upper().replace(".CSV", "")
    destino_encontrado = None

    # Verifica qual substring do mapeamento está presente no nome do arquivo
    for chave, destino_path in mapeamento.items():
        if chave in nome_arquivo:
            destino_encontrado = destino_pathbrlion19
            
            break

    if destino_encontrado is None:
        print(f"⚠️ Nenhum destino encontrado para {arquivo.path}. Pulando.")
        continue

    try:
        # Leitura CSV
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(arquivo.path)

        # Nome do arquivo Parquet final
        nome_base = os.path.basename(arquivo.path).replace(".CSV", "")
        caminho_parquet = f"{destino_encontrado}/{nome_base}.parquet"

        # Escrita Parquet
        df.write.mode("overwrite").parquet(caminho_parquet)
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo.path}: {e}")

print("\n✅ Todos os arquivos foram processados conforme o mapeamento.")
