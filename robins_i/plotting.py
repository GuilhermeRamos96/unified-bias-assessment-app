# utils/plotting.py
import plotly.graph_objects as go
import pandas as pd
# Importar definições de julgamento do robins_i_logic
from .robins_i_logic import ROBINS_I_QUESTIONS, LOW, MODERATE, SERIOUS, CRITICAL, NO_INFO, PENDING

# Mapeamento de julgamentos ROBINS-I para cores
# Usando uma paleta distinta para 4 níveis + NI + Pendente
ROBINS_I_COLOR_MAP = {
    LOW: "#1F77B4",  # Azul (Baixo)
    MODERATE: "#FFBF00",  # Âmbar/Amarelo (Moderado)
    SERIOUS: "#FF7F0E",  # Laranja (Sério)
    CRITICAL: "#D62728",  # Vermelho (Crítico)
    NO_INFO: "#7F7F7F",  # Cinza Médio (Sem Informação)
    PENDING: "#C7C7C7" # Cinza Claro (Pendente)
}

# Ordem dos domínios ROBINS-I para o gráfico
ROBINS_I_DOMAIN_ORDER = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "Geral"]
ROBINS_I_DOMAIN_NAMES = {
    "D1": "Confusão",
    "D2": "Seleção Participantes",
    "D3": "Classificação Intervenções",
    "D4": "Desvios Intervenções",
    "D5": "Dados Faltantes",
    "D6": "Mensuração Desfechos",
    "D7": "Seleção Relato",
    "Geral": "Risco Geral"
}

def criar_grafico_semaforo_robins_i(julgamentos: dict):
    """Cria um gráfico de barras tipo semáforo adaptado para ROBINS-I com Plotly."""
    
    if not julgamentos:
        fig = go.Figure()
        fig.update_layout(title="Gráfico de Risco de Viés ROBINS-I (Aguardando Avaliação)", 
                          xaxis_title="Domínio", yaxis_title="Risco de Viés",
                          yaxis=dict(showticklabels=False),
                          xaxis=dict(categoryorder=\'array\\', categoryarray=[ROBINS_I_DOMAIN_NAMES.get(d, d) for d in ROBINS_I_DOMAIN_ORDER]))
        return fig

    # Prepara os dados para o gráfico
    data = []
    for domain_key in ROBINS_I_DOMAIN_ORDER:
        # Usa PENDING como default se a chave não existir
        judgment = julgamentos.get(domain_key, PENDING) 
        # Garante que mesmo um julgamento inválido tenha uma cor (Pendente)
        color = ROBINS_I_COLOR_MAP.get(judgment, ROBINS_I_COLOR_MAP[PENDING])
        data.append({
            "Domínio": ROBINS_I_DOMAIN_NAMES.get(domain_key, domain_key),
            "Julgamento": judgment,
            "Cor": color,
            "Valor": 1 # Valor fixo para altura da barra
        })
    
    df = pd.DataFrame(data)

    # Cria o gráfico de barras
    fig = go.Figure(go.Bar(
        x=df["Domínio"],
        y=df["Valor"],
        marker_color=df["Cor"],
        text=df["Julgamento"].str.replace("risco ", "R. ").replace("de viés", ""), # Abrevia texto para caber
        textposition="inside",
        insidetextanchor="middle",
        hoverinfo="x+text",
        hovertext=df["Julgamento"], # Mostra texto completo no hover
        width=0.6
    ))

    # Configurações do layout
    fig.update_layout(
        title="Risco de Viés por Domínio (ROBINS-I)",
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            range=[0, 1.2]
        ),
        xaxis=dict(
            categoryorder=\'array\", 
            categoryarray=[ROBINS_I_DOMAIN_NAMES.get(d, d) for d in ROBINS_I_DOMAIN_ORDER],
            tickangle=0 
        ),
        plot_bgcolor=\'rgba(0,0,0,0)\",
        height=350, # Aumenta um pouco a altura para melhor visualização
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Ajusta a fonte do texto dentro das barras
    fig.update_traces(textfont_size=10, textfont_color=\'black\") # Reduz um pouco a fonte

    return fig


