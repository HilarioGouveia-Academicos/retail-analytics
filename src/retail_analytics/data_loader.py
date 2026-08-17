"""Módulo responsável pela ingestão, validação e sanitização dos dados."""

from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
from retail_analytics.config import logger


class DataLoader:
    """Classe responsável pelo carregamento e preparação da base de varejo."""

    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path

    def load_and_clean(self) -> pd.DataFrame:
        """Carrega o arquivo CSV, trata tipos e enriquece colunas temporais."""
        if not self.file_path.exists():
            logger.error(f"Arquivo não encontrado no caminho: {self.file_path}")
            raise FileNotFoundError(f"Arquivo {self.file_path} não existe.")

        try:
            logger.info("Iniciando carregamento do dataset...")
            df = pd.read_csv(self.file_path, sep=";", encoding="utf-8")
            logger.info(f"Dataset carregado com sucesso: {df.shape[0]} linhas e {df.shape[1]} colunas.")

            # Validação e conversão de datas
            if "DATA" in df.columns:
                df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
                df["ANO_MES"] = df["DATA"].dt.to_period("M").astype(str)
                df["DIA_SEMANA"] = df["DATA"].dt.day_name()
            else:
                logger.warning("Coluna 'DATA' não encontrada na base.")

            # Tratamento de decimais brasileiros (ex: '10,50' -> 10.50)
            for col in df.select_dtypes(include=["object"]).columns:
                if df[col].astype(str).str.contains(r"^\d+,\d+$").any():
                    df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

            # Fallback seguro para coluna de faturamento se não existir explicitamente
            if "VALOR_TOTAL" not in df.columns:
                if "QTD" in df.columns and "PRECO_UNIT" in df.columns:
                    df["VALOR_TOTAL"] = df["QTD"] * df["PRECO_UNIT"]
                else:
                    # Cria valor simulado caso a base bruta tenha apenas contagem
                    df["VALOR_TOTAL"] = 1.0

            return df

        except Exception as exc:
            logger.exception("Erro crítico durante a limpeza dos dados.")
            raise RuntimeError(f"Falha no processamento: {exc}") from exc