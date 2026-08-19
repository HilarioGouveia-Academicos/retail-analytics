"""Módulo de configuração e logging centralizado do projeto."""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carrega o .env da raiz
load_dotenv()

# Diretórios base
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Path = BASE_DIR / "data" / "raw"
DATA_FILE_PATH: Path = DATA_DIR / "Base_Varejo.csv"

# Configuração de Logging PEP 8
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("RetailAnalytics")


def get_gemini_api_key() -> str:
    """Recupera a chave da API do Gemini de forma segura via .env ou st.secrets."""
    # 1. Tenta pegar via variável de ambiente / .env
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # 2. Tenta pegar via st.secrets com tratamento seguro caso o arquivo não exista
    try:
        import streamlit as st

        if "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"])
    except Exception:
        pass

    return ""


# --- ADICIONE ESTAS CONFIGURAÇÕES DE API E MODELO AQUI ---
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_GEMINI_MODEL: str = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.6-flash")