"""Encapsulamento de métodos analíticos em Ferramentas (Tools) para o Agente."""

import json
from typing import Any, Dict
import pandas as pd
from retail_analytics.metrics import RetailMetrics
from retail_analytics.config import logger


class RetailAgentTools:
    """Conjunto de ferramentas executáveis pelo modelo de linguagem."""

    def __init__(self, metrics: RetailMetrics) -> None:
        self.metrics = metrics

    def get_macro_kpis(self) -> str:
        """Retorna os principais KPIs de faturamento, cupons, clientes e ticket médio."""
        kpis = self.metrics.get_summary_kpis()
        return json.dumps(kpis, ensure_ascii=False, indent=2)

    def get_top_abc_products(self, top_n: int = 10) -> str:
        """Retorna os top produtos por volume vendido com classificação da Curva ABC."""
        df_abc = self.metrics.calculate_inventory_insights()
        top_df = df_abc.head(top_n)[["PR_NOME", "PR_CAT", "volume_vendido", "curva_abc"]]
        return top_df.to_json(orient="records", force_ascii=False)

    def get_customer_segments_summary(self) -> str:
        """Retorna o resumo de transações e ticket médio por segmento e gênero."""
        mkt_df = self.metrics.calculate_marketing_segments()
        return mkt_df.to_json(orient="records", force_ascii=False)

    def get_category_affinity(self) -> str:
        """Retorna a matriz de compras conjuntas (coocorrência) entre categorias."""
        cooc = self.metrics.calculate_basket_affinity()
        return cooc.to_json()