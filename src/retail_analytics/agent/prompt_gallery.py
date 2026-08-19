"""Módulo centralizador de personas e galeria de prompts de varejo."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PromptTemplate:
    id: str
    title: str
    category: str  # Estoque, Marketing, Pricing, Diretoria
    description: str
    system_prompt: str
    suggested_user_prompt: str


class PromptGallery:
    """Catálogo estruturado de prompts estratégicos para o Agente."""

    @staticmethod
    def get_all_prompts() -> List[PromptTemplate]:
        return [
            PromptTemplate(
                id="stock_optimizer",
                title="📦 Otimizador de Rupturas (Supply Chain)",
                category="Estoque",
                description="Diagnostica itens Classe A em risco de desabastecimento.",
                system_prompt=(
                    "Você é um especialista sênior em Supply Chain e Estoque no varejo. "
                    "Analise os dados da Curva ABC e foque na mitigação de ruptura de itens Classe A, "
                    "identificação de estoque parado de itens Classe C e cálculo de giro."
                ),
                suggested_user_prompt=(
                    "Quais são os 5 principais produtos que mais geram volume e exigem "
                    "atenção imediata de reposição para evitar perda de vendas?"
                ),
            ),
            PromptTemplate(
                id="crm_growth",
                title="🎯 Estrategista de CRM & Campanhas",
                category="Marketing",
                description="Planeja campanhas personalizadas por segmento e presença de filhos.",
                system_prompt=(
                    "Você é o Diretor de Marketing e CRM da rede. Seu foco é maximizar LTV, "
                    "ticket médio e taxa de recompra segmentando por gênero, estado civil e filhos."
                ),
                suggested_user_prompt=(
                    "Gere uma estratégia de campanha promocional de fim de semana "
                    "específica para clientes com filhos do Segmento C."
                ),
            ),
            PromptTemplate(
                id="cross_selling_layout",
                title="🗺️ Arquiteto de Loja & Cross-Selling",
                category="Alocação",
                description="Sugere reorganização de gôndolas com base em afinidade de compras.",
                system_prompt=(
                    "Você é um consultor de Visual Merchandising e Alocação de Espaço em Supermercados. "
                    "Utilize a matriz de coocorrência de cestas para propor mudanças de gôndola."
                ),
                suggested_user_prompt=(
                    "Com base nas categorias mais compradas juntas, quais produtos "
                    "devemos posicionar em pontas de gôndola para aumentar itens por cupom?"
                ),
            ),
            PromptTemplate(
                id="pdf_contract_audit",
                title="📄 Auditor de Documentos & Fornecedores (PDF)",
                category="Auditoria & Compras",
                description="Cruza relatórios em PDF com o comportamento de vendas real.",
                system_prompt=(
                    "Você é um auditor de compras. Compare as tabelas/termos fornecidos no documento PDF "
                    "com as métricas de vendas reais da nossa base para identificar discrepâncias."
                ),
                suggested_user_prompt=(
                    "Analise o PDF anexado e compare os custos ou condições comerciais com o volume vendido desses itens."
                ),
            ),
        ]

    @classmethod
    def get_by_id(cls, prompt_id: str) -> PromptTemplate:
        for prompt in cls.get_all_prompts():
            if prompt.id == prompt_id:
                return prompt
        raise ValueError(f"Prompt com id '{prompt_id}' não encontrado.")