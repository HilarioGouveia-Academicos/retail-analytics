"""Testes unitários para validação das regras de negócio."""

import pandas as pd
import pytest
from retail_analytics.metrics import RetailMetrics


@pytest.fixture
def sample_retail_data() -> pd.DataFrame:
    """Fixture com dados mockados no mesmo formato da Base Varejo."""
    data = {
        "DATA": ["01/02/2019", "01/02/2019", "02/02/2019", "02/02/2019"],
        "CO_ID": [1000, 1000, 1001, 1002],
        "CL_ID": [534, 534, 535, 536],
        "CL_GENERO": ["M", "M", "F", "F"],
        "CL_SEG": ["C", "C", "A", "B"],
        "PR_ID": [1, 2, 1, 3],
        "PR_CAT": ["BEBIDAS", "ALIMENTOS", "BEBIDAS", "LIMPEZA"],
        "PR_NOME": ["GUARANA", "ARROZ", "GUARANA", "DETERGENTE"],
        "VALOR_TOTAL": [10.0, 20.0, 10.0, 5.0],
    }
    return pd.DataFrame(data)


def test_get_summary_kpis(sample_retail_data: pd.DataFrame) -> None:
    metrics = RetailMetrics(sample_retail_data)
    kpis = metrics.get_summary_kpis()

    assert kpis["faturamento_total"] == 45.0
    assert kpis["total_cupons"] == 3
    assert kpis["total_clientes"] == 3
    assert pytest.approx(kpis["ticket_medio"], 0.01) == 15.0


def test_calculate_inventory_abc(sample_retail_data: pd.DataFrame) -> None:
    metrics = RetailMetrics(sample_retail_data)
    abc_df = metrics.calculate_inventory_insights()

    assert "curva_abc" in abc_df.columns
    assert abc_df.iloc[0]["PR_NOME"] == "GUARANA"  # Produto com maior volume