import re
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Sertão Digital",
    page_icon="assets/sertao-digital-icone.png",
    layout="wide",
)


st.markdown("""
<style>

.stApp {
    background-color: #F7FAF9;
}

h1, h2, h3 {
    color: #073B3A;
}

[data-testid="stMetricValue"] {
    color: #007A68;
}

/* Filtros do menu lateral */
div[data-baseweb="select"] {
    cursor: pointer !important;
}

div[data-baseweb="select"] * {
    cursor: pointer !important;
}

div[data-baseweb="select"] > div {
    border: 2px solid #D9E5E3 !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #00A884 !important;
    box-shadow: 0 0 8px rgba(0, 168, 132, 0.25) !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #007A68 !important;
    box-shadow: 0 0 10px rgba(0, 122, 104, 0.35) !important;
}

/* Opções do dropdown */
ul[role="listbox"] li:hover {
    background-color: #E8F7F3 !important;
    color: #007A68 !important;
    cursor: pointer !important;
}

/* Barra de rolagem */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #00A884;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


def limpar_coluna(nome):
    nome = str(nome).strip().replace('"', "").replace("'", "")
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    nome = nome.lower()
    nome = re.sub(r"[^a-z0-9]+", "_", nome)
    return nome.strip("_")


def achar_coluna(df, nomes):
    for nome in nomes:
        if nome in df.columns:
            return nome
    return None


def limpar_texto(serie):
    return (
        serie.astype(str)
        .str.replace('"', "", regex=False)
        .str.replace("'", "", regex=False)
        .str.strip()
    )


def percentual_sim(df, coluna):
    if coluna is None or coluna not in df.columns or len(df) == 0:
        return 0
    return (limpar_texto(df[coluna]).str.lower() == "sim").mean() * 100

def card_kpi(titulo, valor):
    st.markdown(
        f"""
        <div style="
            background-color: #FFFFFF;
            padding: 22px 24px;
            border-radius: 16px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            border: 1px solid #E4ECEA;
            min-height: 135px;
        ">
            <p style="
                margin: 0;
                font-size: 15px;
                color: #1F2937;
                font-weight: 500;
            ">{titulo}</p>
            <h2 style="
                margin-top: 12px;
                margin-bottom: 0;
                color: #007A68;
                font-size: 34px;
                font-weight: 600;
            ">{valor}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


logo = Path("assets/sertao-digital-primaria (1).png")
if not logo.exists():
    logo = Path("assets/sertao-digital-fundo-branco.png")

if logo.exists():
    st.image(str(logo), width=300)


st.title("Portfólio de Mineração de Dados")
st.subheader("Maturidade digital das prefeituras brasileiras")


st.header("Objetivo do Projeto")

st.markdown("""
Este projeto foi desenvolvido como portfólio para a área de **Analista de Dados Júnior**.

O objetivo é analisar o nível de maturidade digital das prefeituras brasileiras utilizando dados abertos do **IBGE - Pesquisa de Informações Básicas Municipais (MUNIC 2024)**.

A aplicação utiliza técnicas de limpeza, preparação, análise exploratória, visualização de dados e comunicação de resultados, simulando uma entrega profissional na área de análise e mineração de dados.
""")


st.header("Pesquisa de Vagas")

st.markdown("""
A vaga escolhida como referência foi **Analista de Dados Júnior**, com foco em mineração, tratamento e visualização de dados.

A partir da análise de vagas do mercado, foram identificadas competências técnicas recorrentes:
""")

vagas = pd.DataFrame({
    "Competência": [
        "Python",
        "SQL",
        "Pandas",
        "Excel",
        "Power BI",
        "Visualização de Dados",
        "Estatística",
        "Comunicação de Resultados",
        "Análise Exploratória de Dados"
    ],
    "Presença nas Vagas": [
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Média",
        "Média",
        "Alta",
        "Alta"
    ],
    "Aplicação neste Projeto": [
        "Utilizado no desenvolvimento da aplicação",
        "Competência relacionada à consulta de bases estruturadas",
        "Utilizado para limpeza e tratamento dos dados",
        "Ferramenta comum para análise inicial de dados",
        "Ferramenta relacionada à criação de dashboards",
        "Utilizado com gráficos interativos",
        "Utilizada na interpretação dos indicadores",
        "Utilizada na geração dos insights",
        "Utilizada para compreensão dos dados municipais"
    ]
})

st.dataframe(vagas, use_container_width=True)


st.header("Sobre a Base de Dados")

st.markdown("""
A base utilizada neste projeto contém informações sobre recursos digitais, infraestrutura tecnológica e canais de atendimento das prefeituras brasileiras.

A escolha dessa base está relacionada à área de interesse em **Governo Digital, Cidades Inteligentes e Transformação Digital Municipal**.

**Fonte:** IBGE - Pesquisa de Informações Básicas Municipais (MUNIC 2024).
""")


df = pd.read_csv("dados/munic_informatica.csv", encoding="utf-8-sig")
df.columns = [limpar_coluna(coluna) for coluna in df.columns]

col_uf = achar_coluna(df, ["uf"])
col_codigo = achar_coluna(df, ["cod_municipio", "codigo_municipio"])
col_municipio = achar_coluna(df, ["municipio", "desc_mun"])
col_populacao = achar_coluna(df, ["populacao"])
col_regiao = achar_coluna(df, ["regiao"])
col_faixa = achar_coluna(df, ["faixa_populacao"])

if col_uf is None:
    st.error("A coluna UF não foi encontrada.")
    st.stop()

df[col_uf] = (
    df[col_uf]
    .astype(str)
    .str.replace('"', "", regex=False)
    .str.replace("'", "", regex=False)
    .str.replace(r"\s+", "", regex=True)
    .str.upper()
)

ufs_validas = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]

df = df[df[col_uf].isin(ufs_validas)].copy()

if col_populacao:
    df[col_populacao] = pd.to_numeric(df[col_populacao], errors="coerce").fillna(0)

col_website = achar_coluna(df, ["atendimento_website", "websites"])
col_whatsapp = achar_coluna(df, ["atendimento_whatsapp", "whatsapp"])
col_tic = achar_coluna(df, ["tem_estrutura_tic", "estrutura_tic",  "tem_estrutura_t"])
col_transparencia = achar_coluna(df, ["tem_portal_transparencia", "portal_da_transparencia"])
col_dados_abertos = achar_coluna(df, ["tem_portal_dados_abertos", "portal_de_dados_abertos"])
col_wifi = achar_coluna(df, ["tem_wifi_publico", "disponibiliza_acesso_por_conexao_wi_fi"])

st.header("Preparação dos Dados")

st.markdown("""
Antes da análise, foram realizados tratamentos para garantir melhor qualidade dos dados.
""")

st.write(f"Total de registros na base tratada: {len(df):,}".replace(",", "."))

st.markdown("""
**Tratamentos realizados:**

- Padronização dos nomes das colunas.
- Remoção de caracteres especiais.
- Normalização das siglas dos estados.
- Conversão da população para formato numérico.
- Filtragem das UFs válidas do Brasil.
- Tratamento de textos para cálculo de indicadores.
""")


st.sidebar.title("Filtros")

ufs = sorted([uf for uf in df[col_uf].dropna().unique() if uf in ufs_validas])
uf_selecionada = st.sidebar.selectbox("Estado", ["Todos"] + ufs)

df_filtrado = df.copy()

if uf_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado[col_uf] == uf_selecionada]

if col_regiao:
    regioes = sorted(df_filtrado[col_regiao].dropna().unique())
    regiao_selecionada = st.sidebar.selectbox("Região", ["Todas"] + regioes)
    if regiao_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado[col_regiao] == regiao_selecionada]

if col_faixa:
    faixas = sorted(df_filtrado[col_faixa].dropna().unique())
    faixa_selecionada = st.sidebar.selectbox("Porte do município", ["Todos"] + faixas)
    if faixa_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado[col_faixa] == faixa_selecionada]


st.write(f"Total de registros após aplicação dos filtros: {len(df_filtrado):,}".replace(",", "."))


total_municipios = df_filtrado[col_codigo].nunique() if col_codigo else len(df_filtrado)
total_ufs = df_filtrado[col_uf].nunique()
populacao_total = df_filtrado[col_populacao].sum() if col_populacao else 0
total_regioes = df_filtrado[col_regiao].nunique() if col_regiao else 0

st.header("Indicadores Gerais")

c1, c2, c3, c4 = st.columns(4)

with c1:
    card_kpi("Municípios", f"{total_municipios:,.0f}".replace(",", "."))

with c2:
    card_kpi("Estados", total_ufs)

with c3:
    card_kpi("População", f"{populacao_total:,.0f}".replace(",", "."))

with c4:
    card_kpi("Regiões", total_regioes)

st.divider()

st.subheader("Indicadores de maturidade digital municipal")

m1, m2, m3, m4 = st.columns(4)

with m1:
    card_kpi("Website", f"{percentual_sim(df_filtrado, col_website):.1f}%")

with m2:
    card_kpi("WhatsApp", f"{percentual_sim(df_filtrado, col_whatsapp):.1f}%")

with m3:
    card_kpi("Estrutura de Tecnologia", f"{percentual_sim(df_filtrado, col_tic):.1f}%")

with m4:
    card_kpi("Transparência", f"{percentual_sim(df_filtrado, col_transparencia):.1f}%")

st.divider()

st.header("Serviços Digitais Municipais")

col_ouvidoria = achar_coluna(df, ["servico_ouvidoria_online"])
col_processos = achar_coluna(df, ["servico_consulta_processos"])
col_nfe = achar_coluna(df, ["servico_nota_fiscal_eletronica"])
col_cpd = achar_coluna(df, ["tem_cpd"])
col_software = achar_coluna(df, ["software_interno"])

s1, s2, s3, s4, s5 = st.columns(5)

with s1:
    card_kpi("Ouvidoria Online", f"{percentual_sim(df_filtrado, col_ouvidoria):.1f}%")

with s2:
    card_kpi("Consulta de Processos", f"{percentual_sim(df_filtrado, col_processos):.1f}%")

with s3:
    card_kpi("Nota Fiscal Eletrônica", f"{percentual_sim(df_filtrado, col_nfe):.1f}%")

with s4:
    card_kpi("Centro de Dados", f"{percentual_sim(df_filtrado, col_cpd):.1f}%")

with s5:
    card_kpi("Software Próprio", f"{percentual_sim(df_filtrado, col_software):.1f}%")



st.markdown("""
<div style="
    margin-top:20px;
    padding:18px;
    background:#F5FAF8;
    border-left:5px solid #00A884;
    border-radius:10px;
">

<h4 style="margin-top:0;color:#007A68;">
📊 Interpretação dos Indicadores
</h4>

Os resultados demonstram que os municípios brasileiros apresentam elevado nível de adoção de canais digitais de atendimento, com destaque para websites institucionais, ouvidorias online e emissão de nota fiscal eletrônica. Em contrapartida, o desenvolvimento de software próprio ainda é uma prática menos comum, indicando oportunidades de fortalecimento da capacidade tecnológica municipal.

</div>
""", unsafe_allow_html=True)

st.divider()

st.header("Análise Exploratória")

g1, g2 = st.columns(2)

if col_regiao:
    dados_regiao = df_filtrado[col_regiao].value_counts().reset_index()
    dados_regiao.columns = ["Região", "Quantidade"]

    fig_regiao = px.bar(
        dados_regiao,
        x="Região",
        y="Quantidade",
        title="Municípios analisados por região",
        color_discrete_sequence=["#007A68"],
    )
    g1.plotly_chart(fig_regiao, use_container_width=True)

if col_website:
    dados_website = df_filtrado[col_website].value_counts().reset_index()
    dados_website.columns = ["Resposta", "Quantidade"]

    fig_website = px.pie(
        dados_website,
        names="Resposta",
        values="Quantidade",
        title="Atendimento por website",
        color_discrete_sequence=["#007A68", "#00D86A", "#F2C94C", "#4B5563"],
    )
    g2.plotly_chart(fig_website, use_container_width=True)


ranking = (
    df_filtrado.groupby(col_uf)
    .size()
    .reset_index(name="Quantidade")
    .sort_values("Quantidade", ascending=False)
)

fig_ranking = px.bar(
    ranking,
    x=col_uf,
    y="Quantidade",
    title="Quantidade de municípios por estado",
    color_discrete_sequence=["#007A68"],
)

st.plotly_chart(fig_ranking, use_container_width=True)


indicadores = {
    "Website": col_website,
    "WhatsApp": col_whatsapp,
    "Estrutura de tecnologia da prefeitura": col_tic,
    "Portal da transparência": col_transparencia,
    "Portal de dados abertos": col_dados_abertos,
    "Wi-Fi público": col_wifi,
}

dados_indicadores = []

for nome, coluna in indicadores.items():
    if coluna:
        dados_indicadores.append({
            "Indicador": nome,
            "Percentual": percentual_sim(df_filtrado, coluna),
        })

if dados_indicadores:
    df_indicadores = pd.DataFrame(dados_indicadores).sort_values("Percentual")

    fig_indicadores = px.bar(
        df_indicadores,
        x="Percentual",
        y="Indicador",
        orientation="h",
        title="Presença de recursos digitais nas prefeituras",
        color_discrete_sequence=["#00D86A"],
        text=df_indicadores["Percentual"].map(lambda x: f"{x:.1f}%"),
    )
    fig_indicadores.update_layout(
        xaxis_title="Percentual de municípios",
        yaxis_title=""
    )
    st.plotly_chart(fig_indicadores, use_container_width=True)


st.markdown("""
<div style="
    padding:20px;
    background:#EAF7F0;
    border-left:5px solid #00A884;
    border-radius:10px;
">

<h4 style="margin-top:0;color:#007A68;">
📈 Principais Descobertas da Análise
</h4>

<b>1.</b> A presença de websites institucionais (86,3%) demonstra que a maioria das prefeituras já possui um canal digital básico de comunicação com a população.<br><br>

<b>2.</b> O WhatsApp está presente em apenas 52,9% dos municípios analisados, indicando potencial de expansão de canais digitais mais acessíveis e utilizados pelos cidadãos.<br><br>

<b>3.</b> Embora 99,7% dos municípios possuam mecanismos de transparência, apenas 60,0% possuem estrutura formal de tecnologia, sugerindo diferenças na capacidade interna de gestão digital.<br><br>

<b>4.</b> Serviços digitais mais avançados apresentam níveis variados de adoção. Enquanto a Nota Fiscal Eletrônica alcança 75,0%, a Consulta de Processos está presente em apenas 44,9% dos municípios.<br><br>

<b>5.</b> Apenas 24,5% dos municípios desenvolvem software próprio, evidenciando forte dependência de fornecedores externos para soluções tecnológicas.<br><br>

<b>6.</b> Os resultados indicam avanços significativos na transformação digital municipal, mas também revelam oportunidades para fortalecimento da infraestrutura tecnológica e ampliação dos serviços digitais oferecidos ao cidadão.

</div>
""", unsafe_allow_html=True)


st.header("Relação com as Competências do Mercado")

st.markdown("""
Este projeto demonstra competências exigidas para vagas de **Analista de Dados Júnior**, como:

- Leitura e preparação de dados com Python.
- Tratamento e padronização com Pandas.
- Criação de dashboards interativos com Streamlit.
- Visualização de dados com Plotly.
- Interpretação de indicadores.
- Comunicação de resultados com foco em tomada de decisão.
""")

st.header("Conclusão")

st.markdown("""
A análise dos dados da pesquisa MUNIC 2024 permitiu identificar o nível de maturidade digital das prefeituras brasileiras.

Os resultados demonstram avanços importantes na adoção de canais digitais de atendimento, transparência pública e disponibilização de informações aos cidadãos.

A utilização de Python, Pandas, Plotly e Streamlit permitiu realizar o processo completo de mineração de dados, desde a preparação dos dados até a geração de insights para apoio à tomada de decisão.
""")

st.divider()

st.subheader("Base de dados tratada")
st.caption("Fonte: IBGE, Pesquisa de Informações Básicas Municipais - MUNIC 2024.")
st.dataframe(df_filtrado, use_container_width=True)