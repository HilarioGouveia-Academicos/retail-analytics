"""Módulo de configuração e logging centralizado do projeto."""

import logging
from pathlib import Path

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