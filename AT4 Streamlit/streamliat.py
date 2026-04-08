import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Painel de Jogos",
    layout="wide",
)

st.title("Painel de Jogos")


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    dados = [
        {"plataforma": "PC", "jogo": "Elden Ring", "genero": "RPG", "preco": 249, "nota": 9.7},
        {"plataforma": "PlayStation 5", "jogo": "God of War Ragnarok", "genero": "Acao", "preco": 299, "nota": 9.6},
        {"plataforma": "Nintendo Switch", "jogo": "Zelda Tears of the Kingdom", "genero": "Aventura", "preco": 357, "nota": 9.8},
        {"plataforma": "Xbox Series X", "jogo": "Forza Horizon 5", "genero": "Corrida", "preco": 199, "nota": 9.2},
        {"plataforma": "PC", "jogo": "Hades", "genero": "Roguelike", "preco": 73, "nota": 9.1},
        {"plataforma": "PlayStation 5", "jogo": "Spider-Man 2", "genero": "Acao", "preco": 349, "nota": 9.0},
    ]

    df = pd.DataFrame(dados)
    df["plataforma"] = df["plataforma"].str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    df["nota"] = pd.to_numeric(df["nota"], errors="coerce")
    df["faixa_preco"] = pd.cut(
        df["preco"],
        bins=[0, 100, 250, 400],
        labels=["Ate R$ 100", "R$ 101 a R$ 250", "R$ 251 a R$ 400"],
        include_lowest=True,
    )
    return df.dropna(subset=["preco", "nota"]).copy()


df = carregar_dados()

st.sidebar.header("Filtros")

plataformas = st.sidebar.multiselect(
    "Selecione as plataformas",
    options=sorted(df["plataforma"].unique()),
    default=sorted(df["plataforma"].unique()),
)

faixa_preco = st.sidebar.slider(
    "Faixa de preco",
    min_value=int(df["preco"].min()),
    max_value=int(df["preco"].max()),
    value=(int(df["preco"].min()), int(df["preco"].max())),
    step=10,
)

df_filtrado = df[
    df["plataforma"].isin(plataformas)
    & df["preco"].between(faixa_preco[0], faixa_preco[1])
].copy()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total de jogos", len(df_filtrado))
kpi2.metric("Preco medio", f"R$ {df_filtrado['preco'].mean():,.0f}".replace(",", "."))
kpi3.metric("Melhor nota", f"{df_filtrado['nota'].max():.1f}")

st.subheader("Tabela de dados")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("Grafico por plataforma")
st.bar_chart(df_filtrado.groupby("plataforma")["preco"].mean())

st.subheader("Grafico por genero")
st.bar_chart(df_filtrado.groupby("genero")["nota"].mean())

st.subheader("Tabela dinamica")
pivot = pd.pivot_table(
    df_filtrado,
    index="plataforma",
    columns="genero",
    values="preco",
    aggfunc="mean",
)
st.dataframe(pivot, use_container_width=True)

st.subheader("Download")
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Baixar CSV filtrado",
    data=csv,
    file_name="jogos_filtrados.csv",
    mime="text/csv",
)
