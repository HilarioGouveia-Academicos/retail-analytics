"""Dashboard Executivo e Operacional em Streamlit."""

"""Aplicação Integrada de Retail Analytics & Decision Copilot."""

import os
import sys
from pathlib import Path

# 1. Garante a resolução correta dos módulos em 'src'
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai
from google.genai import errors

# Importações dos módulos do projeto
from retail_analytics.config import DATA_FILE_PATH, logger
from retail_analytics.data_loader import DataLoader
from retail_analytics.metrics import RetailMetrics
from retail_analytics.agent.prompt_gallery import PromptGallery
from retail_analytics.agent.document_reader import PDFDocumentReader
from retail_analytics.agent.tools import RetailAgentTools

# No topo do app.py:
from retail_analytics.config import (
    DATA_FILE_PATH,
    DEFAULT_GEMINI_MODEL,
    GEMINI_API_KEY,
    logger,
)


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Retail Intelligence & Decision Copilot",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- INJEÇÃO DE CSS CUSTOMIZADO DINÂMICO (SUPORTA LIGHT / DARK / SYSTEM) ---
st.markdown(
    """
    <style>
        /* Estilização dos Cards de Métricas respeitando a cor primária */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: var(--text-color);
            opacity: 0.85;
        }
        
        /* Ajuste visual das abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            font-weight: 600;
            border-radius: 6px 6px 0px 0px;
            padding: 10px 16px;
        }
        
        /* Sidebar usando a cor secundária nativa do tema ativo */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background-color);
            border-right: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        /* Bloco de resposta do Copilot adaptável ao Dark e Light */
        .agent-response {
            background-color: var(--secondary-background-color);
            color: var(--text-color);
            border-left: 4px solid var(--primary-color);
            padding: 14px;
            border-radius: 6px;
            margin-top: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Carrega e sanitiza os dados com cache do Streamlit."""
    loader = DataLoader(DATA_FILE_PATH)
    return loader.load_and_clean()


# Inicialização dos dados
try:
    df = load_data()
    metrics = RetailMetrics(df)
    agent_tools = RetailAgentTools(metrics)
except Exception as exc:
    st.error(f"Erro crítico ao carregar a base de dados: {exc}")
    logger.exception("Falha na inicialização do Streamlit")
    st.stop()


# ==============================================================================
# SIDEBAR: RETAIL COPILOT (ASSISTENTE AGÊNTICO)
# ==============================================================================

with st.sidebar:
    st.title("🤖 Retail Copilot")
    st.caption("Assistente Agêntico com Google Gemini")

    # 1. Recupera a chave do config ou permite input caso esteja vazia
    gemini_api_key = GEMINI_API_KEY
    if not gemini_api_key:
        gemini_api_key = st.text_input(
            "🔑 Insira sua Gemini API Key:",
            type="password",
            help="Ou configure no seu arquivo .env como GEMINI_API_KEY.",
        )

    st.markdown("---")

    # 2. Galeria de Prompts e Personas
    st.subheader("📚 Galeria de Prompts")
    prompts = PromptGallery.get_all_prompts()
    opcoes_prompt = {f"[{p.category}] {p.title}": p for p in prompts}
    escolha = st.selectbox("Selecione um Perfil Especialista:", list(opcoes_prompt.keys()))
    prompt_selecionado = opcoes_prompt[escolha]
    st.info(f"**Foco:** {prompt_selecionado.description}")

    # 3. Upload de Documentos PDF
    st.subheader("📄 Leitor de PDF Auxiliar")
    pdf_file = st.file_uploader(
        "Anexe catálogos, termos comerciais ou faturas:",
        type=["pdf"],
        help="O conteúdo textual do PDF será extraído e injetado no contexto do agente.",
    )

    pdf_context = ""
    if pdf_file:
        try:
            reader = PDFDocumentReader(pdf_file)
            pdf_data = reader.extract_text()
            pdf_context = (
                f"\n\n[CONTEXTO DO DOCUMENTO PDF ({pdf_data['total_pages']} págs)]:\n"
                f"{pdf_data['content'][:4000]}"
            )
            st.success(f"✅ PDF '{pdf_file.name}' indexado!")
        except Exception as err:
            st.error(f"Erro ao ler PDF: {err}")

    # 4. Caixa de Pergunta
    user_query = st.text_area(
        "Instrução ou Pergunta:",
        value=prompt_selecionado.suggested_user_prompt,
        height=120,
    )

    # 5. Localize o botão de execução Agêntica na Sidebar
    if st.button("🚀 Executar Análise", type="primary", use_container_width=True):
        if not gemini_api_key:
            st.warning("⚠️ Forneça uma Gemini API Key para prosseguir.")
        else:
            with st.spinner("Consultando dados e gerando diagnóstico..."):
                try:
                    # 1. Coleta os dados estruturados via Tools
                    contexto_estruturado = f"""
                    --- BASE DE DADOS TRANSACIONAIS ---
                    KPIs Executivos: {agent_tools.get_macro_kpis()}
                    Top Produtos ABC: {agent_tools.get_top_abc_products(10)}
                    Segmentação de Clientes: {agent_tools.get_customer_segments_summary()}
                    {pdf_context}
                    """

                    # 2. DEFINE A VARIÁVEL QUE ESTAVA FALTANDO:
                    prompt_completo = (
                        f"{prompt_selecionado.system_prompt}\n\n"
                        f"Contexto do Varejo:\n{contexto_estruturado}\n\n"
                        f"Pergunta do Usuário:\n{user_query}"
                    )

                    # 3. Inicializa o cliente e faz a chamada
                    client = genai.Client(api_key=gemini_api_key)
                    response = client.models.generate_content(
                        model=DEFAULT_GEMINI_MODEL,
                        contents=prompt_completo,
                    )

                    # 4. Exibe o resultado
                    st.markdown("### 📋 Diagnóstico do Agente:")
                    st.markdown(
                        f"<div class='agent-response'>{response.text}</div>",
                        unsafe_allow_html=True,
                    )

                except errors.APIError as api_err:
                    st.error(f"Erro na API Gemini: {api_err}")
                except Exception as ex:
                    st.error(f"Ocorreu um erro inesperado: {ex}")


# ==============================================================================
# PAINEL PRINCIPAL: DASHBOARDS E DATA STORYTELLING
# ==============================================================================
st.title("📊 Retail Analytics & Decision Intelligence")
st.markdown(
    "Plataforma analítica para exploração de dados de vendas, comportamento de clientes, "
    "otimização de suprimentos e alocação de sortimento."
)

# ----------------------------------------------------
# 1. CARDS DE KPIS MACRO
# ----------------------------------------------------
kpis = metrics.get_summary_kpis()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}")
c2.metric("Total de Cupons", f"{kpis['total_cupons']:,}")
c3.metric("Clientes Únicos", f"{kpis['total_clientes']:,}")
c4.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:.2f}")

st.markdown("---")

# ----------------------------------------------------
# 2. ABAS ANALÍTICAS
# ----------------------------------------------------
tab_estoque, tab_mkt, tab_temporal, tab_alocacao = st.tabs([
    "📦 Gestão de Estoque (Curva ABC)",
    "🎯 Marketing & Segmentação",
    "📈 Temporal & Sazonalidade",
    "🗺️ Alocação & Cross-Selling",
])

# --- ABA 1: ESTOQUE ---
with tab_estoque:
    st.subheader("Otimização de Ruptura e Reposição de Estoque")
    st.write(
        "Classificação dos produtos por volume de saída para guiar o abastecimento "
        "e a gestão de espaço em armazém."
    )
    abc_df = metrics.calculate_inventory_insights()

    col_pie, col_bar = st.columns([1, 2])
    with col_pie:
        fig_abc = px.pie(
            abc_df,
            names="curva_abc",
            title="Distribuição por Classe ABC",
            hole=0.45,
            color="curva_abc",
            color_discrete_map={"A": "#22c55e", "B": "#eab308", "C": "#ef4444"},
        )
        st.plotly_chart(fig_abc, use_container_width=True)

    with col_bar:
        top_produtos = abc_df.head(10)
        fig_bar = px.bar(
            top_produtos,
            x="volume_vendido",
            y="PR_NOME",
            orientation="h",
            color="PR_CAT",
            title="Top 10 Produtos em Volume (Giro Rápido)",
            labels={"volume_vendido": "Qtd. Vendida", "PR_NOME": "Produto"},
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)

# --- ABA 2: MARKETING ---
with tab_mkt:
    st.subheader("Perfil de Compras por Segmento e Gênero")
    mkt_df = metrics.calculate_marketing_segments()

    fig_mkt = px.bar(
        mkt_df,
        x="CL_SEG",
        y="ticket_medio",
        color="CL_GENERO",
        barmode="group",
        title="Ticket Médio por Faixa de Segmento e Gênero",
        labels={"ticket_medio": "Ticket Médio (R$)", "CL_SEG": "Segmento de Cliente"},
    )
    st.plotly_chart(fig_mkt, use_container_width=True)

# --- ABA 3: TEMPORAL & SAZONALIDADE ---
with tab_temporal:
    st.subheader("Padrões Temporais de Vendas e Concentração Semanal")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        if "ANO_MES" in df.columns:
            evolucao_mensal = (
                df.groupby("ANO_MES")
                .agg(cupons=("CO_ID", "nunique"), faturamento=("VALOR_TOTAL", "sum"))
                .reset_index()
                .sort_values(by="ANO_MES")
            )
            fig_mensal = px.line(
                evolucao_mensal,
                x="ANO_MES",
                y="cupons",
                markers=True,
                title="Evolução Mensal de Transações (Cupons)",
                labels={"ANO_MES": "Mês/Ano", "cupons": "Qtd. Cupons"},
            )
            st.plotly_chart(fig_mensal, use_container_width=True)

    with col_t2:
        if "DIA_SEMANA" in df.columns:
            dias_ordem = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            df_semana = (
                df.groupby("DIA_SEMANA", observed=False)["CO_ID"]
                .nunique()
                .reindex(dias_ordem)
                .reset_index()
            )
            df_semana["DIA_PT"] = [
                "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"
            ]
            fig_dia = px.bar(
                df_semana,
                x="DIA_PT",
                y="CO_ID",
                title="Concentração de Transações por Dia da Semana",
                labels={"DIA_PT": "Dia da Semana", "CO_ID": "Qtd. Cupons"},
                color="CO_ID",
                color_continuous_scale="Blues",
            )
            st.plotly_chart(fig_dia, use_container_width=True)

# --- ABA 4: ALOCAÇÃO & CROSS-SELLING ---
with tab_alocacao:
    st.subheader("Matriz de Afinidade de Categorias (Cesta de Compras)")
    st.write(
        "Identifica a frequência com que categorias distintas foram incluídas "
        "na mesma cesta de compras (`CO_ID`)."
    )
    cooc_matrix = metrics.calculate_basket_affinity()

    fig_heat = px.imshow(
        cooc_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Coocorrência entre Categorias",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_heat, use_container_width=True)