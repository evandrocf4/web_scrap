import csv
import random

# Definição dos cenários e intervalos de valores
cenarios = [
    ("Sem Particionamento", 547, 89, 92, 41.30),
    ("Particionamento Tradicional", 327, 66, 74, 29.10),
    ("Liquid Clustering", 212, 48, 59, 19.85),
]

# Gerar dados aleatórios dentro dos intervalos especificados
num_consultas = 20
dados = []

for cenario, tempo_medio, uso_cpu, uso_memoria, custo_estimado in cenarios:
    for consulta in range(1, num_consultas + 1):
        dados.append([
            cenario,
            consulta,
            round(random.uniform(tempo_medio * 0.9, tempo_medio * 1.1), 2),
            round(random.uniform(uso_cpu * 0.9, uso_cpu * 1.1), 2),
            round(random.uniform(uso_memoria * 0.9, uso_memoria * 1.1), 2),
            round(random.uniform(custo_estimado * 0.9, custo_estimado * 1.1), 2),
        ])

# Escrever os dados em um arquivo CSV
nome_arquivo = "dados_consultas.csv"
with open(nome_arquivo, mode="w", newline="") as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerow(["Cenario", "Consulta", "Tempo", "Uso_CPU", "Uso_Mem", "Custo"])
    escritor.writerows(dados)

print(f"Arquivo {nome_arquivo} gerado com sucesso!")