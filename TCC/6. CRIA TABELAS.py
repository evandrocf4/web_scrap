from pyspark.sql.functions import input_file_name, regexp_extract
from pyspark.sql.types import StringType
import os

# Catálogo e schema (ajuste se necessário)
catalogo = "especializacao"
schema = "landing"

# Dicionário com nome da tabela e diretório de origem
mapeamento = {
    "cnae": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/cnaes",
    "simples_nacional": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/simples",
    "motivacoes": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/motivos",
    "municipios": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/municipios",
    "naturezas_juridicas": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/naturezas",
    "paises": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/paises",
    "qualificacoes": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/qualificacoes",
    "empresas": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/empresas",
    "estabelecimentos": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/estabelecimentos",
    "socios": "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/socios"
}

# Cria o schema no Unity Catalog, se necessário
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalogo}.{schema}")

# Loop para processar cada dataset
for nome_tabela, caminho_origem in mapeamento.items():
    print(f"🔄 Processando tabela: {nome_tabela}")

    try:
        # Testa se existem arquivos no diretório
        arquivos = dbutils.fs.ls(caminho_origem)
        arquivos_parquet = [f.path for f in arquivos if f.path.endswith(".parquet")]

        if not arquivos_parquet:
            print(f"⚠️ Nenhum arquivo Parquet encontrado em {caminho_origem}. Pulando...")
            continue

        # Leitura dos arquivos com inferência de schema
        df = (
            spark.read.format("parquet")
            .load(caminho_origem)
            .withColumn("file_name", input_file_name())
            .withColumn("ano_mes", regexp_extract("file_name", r'(\d{4}-\d{2})', 1).cast(StringType()))
            .drop("file_name")
        )

        # Caminho Delta
        caminho_delta = caminho_origem.replace("/raw/", "/delta/")
        tabela_completa = f"{catalogo}.{schema}.{nome_tabela}"

        # Escrita particionada por ano_mes
        (
            df.write
            .format("delta")
            .mode("overwrite")
            .option("overwriteSchema", "true")
            .clusterBy("ano_mes")
            .option("path", caminho_delta)
            .saveAsTable(tabela_completa)
        )

        print(f"✅ Tabela {tabela_completa} criada com sucesso!\n")

    except Exception as e:
        print(f"❌ Erro ao processar {nome_tabela}: {str(e)}\n")
