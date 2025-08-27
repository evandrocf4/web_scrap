from tqdm import tqdm
# Diretórios a serem limpos

paths_para_limpar = [
    "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/raw",
    "abfss://landing@gen2especializacao.dfs.core.windows.net/raw/landing"
]

for path in paths_para_limpar:
    print(f"\n🧹 Limpando: {path}")
    
    try:
        arquivos_ou_pastas = dbutils.fs.ls(path)
        
        for item in tqdm(arquivos_ou_pastas, desc=f"🚨 Removendo de {path}"):
            dbutils.fs.rm(item.path, recurse=True)
        
        print(f"✅ Limpeza finalizada para: {path}")
    except Exception as e:
        print(f"❌ Erro ao limpar {path}: {e}")
