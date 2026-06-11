import streamlit as st
import pandas as pd
import plotly.express as px
 
st.title("Meu Primeiro Dashboard de IDEB")
 
df = pd.read_csv("escolas.csv")
 
with st.sidebar:
    st.subheader("Filtros")
    regioes = df["Regiao"].unique()
    opcao = st.selectbox(
        "Selecione a Região", regioes
    )
 
    df_regiao = df[df["Regiao"] == opcao]
    ufs_disponiveis = df_regiao["UF"].unique()
    ufs_selecionadas = st.multiselect(
        "Selecione as UFs",
        ufs_disponiveis,
        default=list(ufs_disponiveis)
    )
 
    min_alunos = int(df["Alunos"].min())
    max_alunos = int(df["Alunos"].max())
    limite_alunos = st.slider(
        "Mínimo de Alunos",
        min_alunos,
        max_alunos,
        min_alunos
    )
 
# Aplicar filtros
df_filtrado = df_regiao[
    df_regiao["UF"].isin(ufs_selecionadas)
]
df_filtrado = df_filtrado[
    df_filtrado["Alunos"] >= limite_alunos
]
 
# Métricas
col1, col2 = st.columns(2)
with col1:
    media_2023 = df_filtrado["IDEB_2023"].mean()
    media_2021 = df_filtrado["IDEB_2021"].mean()
    delta = media_2023 - media_2021
    st.metric(
        "Média IDEB 2023",
        f"{media_2023:.2f}",
        delta=f"{delta:+.2f}"
    )
with col2:
    total_alunos = df_filtrado["Alunos"].sum()
    st.metric(
        "Total de Alunos",
        f"{total_alunos:,}"
    )
 
# Abas
aba1, aba2 = st.tabs(
    ["Gráfico de Barras", "Evolução Temporal"]
)
 
with aba1:
    fig = px.bar(
        df_filtrado,
        x="Escola",
        y="IDEB_2023",
        color="IDEB_2023",
        color_continuous_scale="Viridis",
        title="IDEB das Escolas"
    )
    st.plotly_chart(fig, use_container_width=True)
 
with aba2:
    df_melted = df_filtrado.melt(
        id_vars=["Escola"],
        value_vars=["IDEB_2021", "IDEB_2023"],
        var_name="Ano",
        value_name="IDEB"
    )
    df_melted["Ano"] = df_melted["Ano"].str.replace(
        "IDEB_", ""
    )
    fig_line = px.line(
        df_melted,
        x="Ano",
        y="IDEB",
        color="Escola",
        markers=True,
        title="Evolução do IDEB (2021 vs 2023)"
    )
    st.plotly_chart(fig_line, use_container_width=True)
