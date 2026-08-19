# 🛒 Retail Analytics & Decision Copilot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/GenAI-Gemini%203.6-8E75C2.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Plataforma inteligente de **Engenharia de Dados e Tomada de Decisão (Decision Intelligence)** voltada ao setor supermercadista/varejista. O projeto combina pipelines analíticos robustos (seguindo PEP 8, Type Hints e testes automatizados) com um **Assistente Agêntico (Retail Copilot)** movido pelo Google Gemini.

---

## 🎯 Pilares Estratégicos de Varejo

* **📦 Gestão de Estoque:** Curva ABC de produtos para priorização de reposição e mitigação de rupturas de itens Classe A[cite: 3].
* **🎯 Marketing & Segmentação:** Clusterização demográfica (`CL_SEG`, gênero e presença de dependentes) e análise de ticket médio[cite: 3].
* **📈 Temporal & Sazonalidade:** Monitoramento de sazonalidade mensal e concentração de transações por dia da semana[cite: 3].
* **🗺️ Alocação de Produtos (Cross-Selling):** Matriz de afinidade e coocorrência de compras no mesmo cupom fiscal[cite: 3].
* **🤖 Retail Copilot (Agente IA):** Assistente agêntico para diagnósticos com suporte a leitura e cruzamento de relatórios em **PDF**[cite: 3].

---

## 🧱 Arquitetura do Repositório

```text
retail_analytics/
├── data/
│   └── raw/
│       └── Base_Varejo.csv          # Base transacional (830k linhas)
├── src/
│   └── retail_analytics/
│       ├── __init__.py
│       ├── config.py                # Logging e variáveis de ambiente
│       ├── data_loader.py           # Ingestão e sanitização de dados (POO)
│       ├── metrics.py               # Motores analíticos de varejo
│       └── agent/
│           ├── __init__.py
│           ├── document_reader.py   # Extração textual de PDFs (PyPDF)
│           ├── prompt_gallery.py    # Galeria de Personas e Prompts
│           └── tools.py             # Tools estruturadas para a LLM
├── tests/
│   ├── __init__.py
│   └── test_metrics.py              # Testes unitários com Pytest
├── app.py                           # Interface Streamlit com Copilot
├── pyproject.toml                   # Metadados e configuração de testes
├── requirements.txt                 # Dependências versionadas
├── LICENSE                          # Licença MIT
├── README.md                        # Apresentação do repositório
└── DOCUMENTACAO_EXECUTIVA_RETAIL.md # Relatório executivo e governança técnica
```[cite: 3]

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Criar Ambiente Virtual

```bash
git clone <URL_DO_REPOSITORIO>
cd retail_analytics

# Criar e ativar ambiente virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```[cite: 3]

### 2. Instalar Dependências e o Pacote Local

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```[cite: 3]

### 3. Configurar a Chave da API do Gemini

Crie um arquivo `.env` na raiz do projeto (ou configure no `.streamlit/secrets.toml`):

```env
GEMINI_API_KEY="sua_chave_do_google_aistudio"
GEMINI_MODEL_NAME="gemini-3.6-flash"
```[cite: 3]

### 4. Executar os Testes Automatizados

```bash
pytest tests/ -v
```[cite: 3]

### 5. Iniciar o Dashboard & Copilot

```bash
streamlit run app.py
```[cite: 3]

---

## 📄 Documentação Complementar

Para uma análise detalhada dos pilares de negócio, governança de dados e arquitetura técnica, consulte o arquivo [DOCUMENTACAO_EXECUTIVA_RETAIL.md](DOCUMENTACAO_EXECUTIVA_RETAIL.md)[cite: 3].

---

## ⚖️ Licença

Este projeto está sob a licença [MIT](LICENSE)[cite: 3].