import pandas as pd


df = pd.read_csv("livros.csv", sep=";")

print("Primeiras 5 linhas")
print(df.head())

print("\nEstrutura do dataset")
df.info()

print("\nResumo estatistico")
print(df.describe(include="all"))

print("\nColunas com tipo possivelmente incorreto:")
print("- isbn: veio como float64, mas normalmente deve ser texto.")
print("- ano: veio como float64 por causa de valor nulo; pode ser inteiro anulavel (Int64).")

print("\nValores nulos por coluna")
resumo_nulos = df.isnull().sum().reset_index()
resumo_nulos.columns = ["coluna", "valores_nulos"]
print(resumo_nulos)

print("\n Livros com 0 paginas")
livros_zero_paginas = df[df["paginas"] == 0]
print(f"Quantidade: {len(livros_zero_paginas)}")
print(livros_zero_paginas)

print("\nQuantidade de livros por ano")
livros_por_ano = df["ano"].value_counts().sort_index()
print(livros_por_ano)

print("\nFaixa de paginas")
df["faixa_paginas"] = df["paginas"].apply(
    lambda x: "Curto" if x < 150 else "Médio" if x <= 350 else "Longo"
)
print(df[["paginas", "faixa_paginas"]].head())

print("\nLimpeza de registros com 0 paginas")
df_limpo = df[df["paginas"] > 0].copy()
removidos = len(df) - len(df_limpo)
print(f"Registros removidos: {removidos}")

print("\nTratamento da coluna ano")
mediana_ano = df_limpo["ano"].median()
df_limpo["ano"] = df_limpo["ano"].fillna(mediana_ano).astype(int)
print(f"Mediana usada para preencher nulos: {int(mediana_ano)}")
print(df_limpo["ano"].head())

print("\nDecada de publicacao")
df_limpo["decada"] = (df_limpo["ano"] // 10) * 10
print(df_limpo[["ano", "decada"]].head())
