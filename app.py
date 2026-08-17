"""Dashboard Executivo e Operacional em Streamlit."""

import plotly.express as px
import streamlit as st
from retail_analytics.config import DATA_FILE_PATH, logger
from retail_analytics.data_loader import DataLoader
from retail_analytics.metrics import RetailMetrics

# Configuração da Página
st.set_page_config(
    page_title="Retail Insights & Strategy",
    page_icon="🛒",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_data():
    loader = DataLoader(DATA_FILE_PATH)
    return loader.load_and_clean()


st.title("🛒 Retail Insights: Estoque, Marketing e Alocação")
st.caption("Data Storytelling analítico para suporte à tomada de decisão no varejo.")

try:
    df = load_data()
    metrics = RetailMetrics(df)
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# ----------------------------------------------------
# 1. VISÃO EXECUTIVA (KPIs)
# ----------------------------------------------------
kpis = metrics.get_summary_kpis()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento", f"R$ {kpis['faturamento_total']:,.2f}")
col2.metric("Total de Cupons", f"{kpis['total_cupons']:,}")
col3.metric("Clientes Únicos", f"{kpis['total_clientes']:,}")
col4.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:.2f}")

st.markdown("---")

# ----------------------------------------------------
# 2. ABAS TEMÁTICAS DE NEGÓCIO
# ----------------------------------------------------
tab_estoque, tab_mkt, tab_alocacao = st.tabs([
    "📦 Gestão de Estoque (Curva ABC)",
    "🎯 Marketing & Segmentação",
    "🗺️ Alocação & Cross-Selling",
])

with tab_estoque:
    st.subheader("Otimização de Ruptura e Reposição de Estoque")
    st.write(
        "Identificação dos itens **Classe A** que exigem maior acurácia de reposição "
        "e dos itens **Classe C** candidatos a redução de estoque."
    )
    abc_df = metrics.calculate_inventory_insights()

    c1, c2 = st.columns([1, 2])
    with c1:
        fig_abc = px.pie(
            abc_df,
            names="curva_abc",
            title="Distribuição de Itens por Classe ABC",
            hole=0.4,
            color="curva_abc",
            color_discrete_map={"A": "#2ecc71", "B": "#f1c40f", "C": "#e74c3c"},
        )
        st.plotly_chart(fig_abc, use_container_width=True)

    with c2:
        top_produtos = abc_df.head(10)
        fig_bar = px.bar(
            top_produtos,
            x="volume_vendido",
            y="PR_NOME",
            orientation="h",
            color="PR_CAT",
            title="Top 10 Produtos por Demanda (Giro)",
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_mkt:
    st.subheader("Estratégias de Campanhas e Precificação por Perfil")
    mkt_df = metrics.calculate_marketing_segments()

    fig_mkt = px.bar(
        mkt_df,
        x="CL_SEG",
        y="ticket_medio",
        color="CL_GENERO",
        barmode="group",
        title="Ticket Médio por Segmento e Gênero de Cliente",
        labels={"ticket_medio": "Ticket Médio (R$)", "CL_SEG": "Segmento"},
    )
    st.plotly_chart(fig_mkt, use_container_width=True)

with tab_alocacao:
    st.subheader("Layout de Loja e Posicionamento de Gôndolas")
    st.write(
        "Matriz de afinidade entre categorias para organizar o fluxo físico "
        "e impulsionar compras combinadas."
    )
    cooc_matrix = metrics.calculate_basket_affinity()

    fig_heat = px.imshow(
        cooc_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Afinidade (Categorias compradas juntas no mesmo cupom)",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_heat, use_container_width=True)