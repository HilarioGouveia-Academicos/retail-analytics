# Relatório Executivo e Documentação Técnica: Retail Analytics & Decision Intelligence

---

## 1. Sumário Executivo

Este projeto estabelece uma infraestrutura moderna de **Engenharia, Análise e Ciência de Dados** voltada ao setor supermercadista/varejista, utilizando técnicas avançadas de análise exploratória, modelagem de dados, arquitetura em camadas e visualização orientada a **Data Storytelling**.

A partir de uma base transacional de **830.000 registros**, o sistema endereça os quatro pilares estratégicos de rentabilidade e eficiência no varejo:
1. **Gestão e Otimização de Estoque:** Minimização de rupturas e excessos através da Curva ABC de giro e volume.
2. **Segmentação e Estratégia de Marketing:** Clusterização demográfica e comportamental para personalização de campanhas.
3. **Estratégia de Precificação e Rentabilidade:** Análise de sensibilidade, elasticidade e monitoramento de ticket médio por perfil.
4. **Alocação de Produtos e Merchandising Visual:** Otimização de gôndolas e cross-selling baseada em matrizes de afinidade de compras (*Market Basket Analysis*).

---

## 2. Pilares Estratégicos de Negócio

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RETAIL DECISION ENGINE                                │
└────────┬───────────────────┬─────────────────────┬───────────────────┬──────────┘
         │                   │                     │                   │
         ▼                   ▼                     ▼                   ▼
 ┌───────────────┐   ┌───────────────┐     ┌───────────────┐   ┌───────────────┐
 │ 1. ESTOQUE    │   │ 2. MARKETING  │     │ 3. PREÇOS     │   │ 4. ALOCAÇÃO   │
 ├───────────────┤   ├───────────────┤     ├───────────────┤   ├───────────────┤
 │ • Curva ABC   │   │ • Perfis SEG  │     │ • Ticket Médio│   │ • Coocorrência│
 │ • Giro Rápido │   │ • Gênero/Filho│     │ • Sensibilidad│   │ • Cross-Sell  │
 │ • Anti-Ruptura│   │ • Retenção    │     │ • Margem Alvo │   │ • Gôndolas    │
 └───────────────┘   └───────────────┘     └───────────────┘   └───────────────┘
```

### 2.1 Gestão de Estoque (Curva ABC & Prevenção de Ruptura)
* **Objetivo:** Garantir que o capital de giro esteja alocado nos produtos com maior impacto no volume e receita.
* **Metodologia:** Classificação de itens em:
  * **Classe A (Top 70% do volume):** Itens essenciais (ex: arroz, refrigerantes, itens de cesta básica). Requerem reabastecimento contínuo (*just-in-time*), contratos de fornecimento garantido e alertas rígidos contra ruptura.
  * **Classe B (20% seguintes):** Produtos intermediários com demanda previsível.
  * **Classe C (10% finais):** Produtos de cauda longa. Devem ter estoque mínimo reduzido para evitar obsolescência e custos desnecessários de armazenagem.

### 2.2 Estratégias de Marketing e Segmentação de Clientes
* **Objetivo:** Migrar de uma comunicação genérica de massa para ofertas hiper-personalizadas.
* **Metodologia:** Cruzamento dos atributos cadastrais (`CL_SEG`, `CL_GENERO`, `CL_FHL` - Filhos) com hábitos de consumo.
  * *Exemplo prático:* Clientes com filhos e ticket médio elevado recebem promoções focadas em categorias de higiene infantil e alimentação familiar, enquanto segmentos de alta frequência recebem programas de fidelidade.

### 2.3 Precificação e Rentabilidade
* **Objetivo:** Otimizar as margens sem prejudicar o volume de tráfego na loja.
* **Metodologia:** Análise de dispersão de preços e variação do ticket médio por cupom fiscal (`CO_ID`). Identificação de produtos âncora (geradores de fluxo) versus produtos de margem (rentabilizadores de cesta).

### 2.4 Alocação de Produtos e Layout de Loja (*Cross-Selling*)
* **Objetivo:** Aumentar o número de itens por cupom através do posicionamento estratégico de categorias.
* **Metodologia:** Matriz de coocorrência de produtos e categorias no mesmo cupom fiscal. Identificação de padrões naturais de compra associada (ex: *Bebidas + Petiscos*, *Massas + Molhos*, *Itens de Limpeza + Higiene*) para posicionamento adjacente nas gôndolas ou displays de ponta de ilha.

---

## 3. Arquitetura da Solução & Boas Práticas (PEP 8 & Clean Code)

A solução segue estritamente as diretrizes de engenharia de software modernas para aplicações analíticas:

```
retail_analytics/
├── data/
│   └── raw/
│       └── Base_Varejo.csv          # Base bruta com separador ';' e 830k linhas
├── src/
│   └── retail_analytics/
│       ├── __init__.py              # Exportações do pacote
│       ├── config.py                # Configuração centralizada de paths e Logging
│       ├── data_loader.py           # Ingestão, sanitização e tipagem (POO)
│       └── metrics.py               # Motores analíticos de negócio (ABC, Mkt, Basket)
├── tests/
│   ├── __init__.py
│   └── test_metrics.py              # Testes unitários automatizados (Pytest)
├── app.py                           # Dashboard interativo com Data Storytelling (Streamlit)
├── pyproject.toml                   # Especificação do pacote e configuração do Pytest
├── requirements.txt                 # Dependências versionadas
└── README.md                        # Documentação técnica e guia de execução
```

### Padrões Técnicos Aplicados:
1. **Tipagem Estática (PEP 484):** Uso de `Type Hints` em todas as assinaturas de funções e métodos (`pd.DataFrame`, `Dict[str, float]`, `Path`, etc.), facilitando a manutenção e reduzindo bugs de execução.
2. **Orientação a Objetos (POO):** Encapsulamento de responsabilidades em classes dedicadas (`DataLoader` para I/O e tratamento; `RetailMetrics` para cálculos de negócio).
3. **Centralized Logging:** Rastreabilidade estruturada de passos de execução, volumetria carregada e alertas de dados inválidos sem uso de `print()`.
4. **Resolução de Caminhos Portáveis (`pathlib.Path`):** Compatibilidade nativa em Windows, macOS e Linux sem caminhos hardcoded.
5. **Automação de Testes (`pytest`):** Cobertura de regras críticas de agregação e KPIs com fixtures representativas.

---

## 4. Dicionário de Dados

| Campo | Tipo Lógico | Descrição e Aplicação Estratégica |
| :--- | :--- | :--- |
| **`DATA`** | Datetime | Data da emissão do cupom fiscal. Usada para análise de sazonalidade e dia da semana. |
| **`CO_ID`** | Integer / String | Identificador exclusivo do cupom (cesta de compras). Base para métricas de ticket e coocorrência. |
| **`CL_ID`** | Integer / String | Identificador único do cliente cadastrado. Permite métricas de frequência, recência e LTV. |
| **`CL_GENERO`**| Categórico (`M`/`F`) | Gênero do cliente para segmentação demográfica de marketing. |
| **`CL_EC`** | Categórico / Numérico | Estado civil do cliente. |
| **`CL_FHL`** | Numérico | Indicador / quantidade de filhos. Direciona campanhas de produtos infantis e família. |
| **`CL_SEG`** | Categórico (`A`,`B`,`C`)| Segmento ou faixa de renda/fidelidade do cliente. |
| **`PR_ID`** | Integer / String | Código único identificador do produto vendido. |
| **`PR_CAT`** | Categórico | Categoria macro do item (`ALIMENTOS`, `BEBIDAS`, `HIGIENE`, `LIMPEZA`). |
| **`PR_NOME`**| Texto | Descrição do produto para visualização executiva e curva ABC. |
| **`VALOR_TOTAL`**| Numérico (Float) | Faturamento gerado pelo item na transação. |

---

## 5. Guia de Instalação e Execução

### Pré-requisitos
* Python 3.10 ou superior
* Gerenciador de pacotes `pip`

### Passo a Passo

1. **Clonar/Estruturar o projeto:**
   ```bash
   git clone <https://github.com/HilarioGouveia-Academicos/retail-analytics>
   cd retail_analytics
   ```

2. **Criar e ativar o ambiente virtual:**
   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Executar a suíte de testes unitários:**
   ```bash
   pytest
   ```

5. **Iniciar a aplicação interativa de Data Storytelling (Streamlit):**
   ```bash
   streamlit run app.py
   ```

---

## 6. Conclusões e Recomendações Estratégicas

1. **Automatização de Compras (Estoque):** Integrar o cálculo da Curva ABC ao software de ERP para parametrização automática de ponto de pedido e estoque de segurança para produtos Classe A.
2. **Campanhas Segmentadas (Marketing):** Disparar ofertas via WhatsApp/App direcionadas por perfil (`CL_SEG` + presença de filhos) em dias de maior tração da semana.
3. **Revisão de Layout (Alocação):** Reposicionar produtos de alta afinidade de categorias complementares em ilhas centrais para elevar o ticket médio e a profundidade da cesta.

---

## 7. Autor

**Hilário Félix de Gouveia Junior**

- GitHub: (https://github.com/HilarioGouveia)
- LinkedIn: (https://linkedin.com/in/hilário-gouveia-30a09b26b)
- E-mail: hilario.tantra@gmail.com

---
*Documento homologado para apresentação executiva e governança técnica da equipe de Engenharia de Dados & Analytics.*



echo "# retail-analytics" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/HilarioGouveia-Academicos/retail-analytics.git
git push -u origin main