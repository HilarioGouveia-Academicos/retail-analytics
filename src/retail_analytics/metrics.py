"""Módulo de cálculo de métricas para Gestão de Estoque, Marketing, Preço e Alocação."""

from typing import Dict
import pandas as pd
from retail_analytics.config import logger


class RetailMetrics:
    """Motor analítico de métricas de varejo."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data

    def calculate_inventory_insights(self) -> pd.DataFrame:
        """Estoque: Curva ABC por volume e faturamento para orientar reposição."""
        logger.info("Calculando métricas de estoque (Curva ABC)...")
        abc = (
            self.data.groupby(["PR_CAT", "PR_NOME"], as_index=False)
            .agg(
                volume_vendido=("PR_ID", "count"),
                faturamento_total=("VALOR_TOTAL", "sum"),
            )
            .sort_values(by="volume_vendido", ascending=False)
        )
        abc["share_acumulado"] = (
            abc["volume_vendido"].cumsum() / abc["volume_vendido"].sum()
        )
        abc["curva_abc"] = abc["share_acumulado"].apply(
            lambda x: "A" if x <= 0.7 else ("B" if x <= 0.9 else "C")
        )
        return abc

    def calculate_marketing_segments(self) -> pd.DataFrame:
        """Marketing: Perfil do cliente e valor por segmento demográfico."""
        logger.info("Calculando métricas de marketing e perfil de clientes...")
        return (
            self.data.groupby(["CL_SEG", "CL_GENERO"], as_index=False)
            .agg(
                total_clientes=("CL_ID", "nunique"),
                total_transacoes=("CO_ID", "nunique"),
                faturamento=("VALOR_TOTAL", "sum"),
            )
            .assign(
                ticket_medio=lambda x: x["faturamento"] / x["total_transacoes"]
            )
        )

    def calculate_basket_affinity(self) -> pd.DataFrame:
        """Alocação de Produtos: Coocorrência de categorias na mesma compra."""
        logger.info("Calculando afinidade entre categorias para alocação...")
        basket = (
            self.data.groupby(["CO_ID", "PR_CAT"])["PR_ID"]
            .count()
            .unstack()
            .fillna(0)
        )
        # Binarização da presença da categoria no cupom
        basket_binary = basket.map(lambda x: 1 if x > 0 else 0)
        # Matriz de coocorrência (Afinidade)
        co_occurrence = basket_binary.T.dot(basket_binary)
        return co_occurrence

    def get_summary_kpis(self) -> Dict[str, float]:
        """Retorna os KPIs macro para visão executiva."""
        total_faturamento = float(self.data["VALOR_TOTAL"].sum())
        total_cupons = int(self.data["CO_ID"].nunique())
        total_clientes = int(self.data["CL_ID"].nunique())
        ticket_medio = total_faturamento / total_cupons if total_cupons > 0 else 0.0

        return {
            "faturamento_total": total_faturamento,
            "total_cupons": total_cupons,
            "total_clientes": total_clientes,
            "ticket_medio": ticket_medio,
        }