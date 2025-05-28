# utils/plotting.py
import plotly.graph_objects as go
import pandas as pd
from .rob2_logic import ROB2_QUESTIONS, LOW, SOME_CONCERNS, HIGH, PENDING

# Mapeamento de julgamentos para cores (padrão semáforo)
COLOR_MAP = {
    LOW: "#2ca02c",  # Verde
    SOME_CONCERNS: "#ffdd00",  # Amarelo
    HIGH: "#d62728",  # Vermelho
    PENDING: "#cccccc" # Cinza para pendente
}

# Ordem dos domínios para o gráfico
DOMAIN_ORDER = ["D1", "D2", "D3", "D4", "D5", "Geral"]
DOMAIN_NAMES = {
    "D1": "Randomização",
    "D2": "Desvios Intervenção",
    "D3": "Dados Ausentes",
    "D4": "Mensuração Desfecho",
    "D5": "Seleção Relato",
    "Geral": "Risco Geral"
}

def criar_grafico_semaforo(julgamentos: dict):
    """Cria um gráfico de barras tipo semáforo com Plotly."""
    
    if not julgamentos:
        # Retorna um gráfico vazio ou uma mensagem se não houver julgamentos
        fig = go.Figure()
        fig.update_layout(title="Gráfico de Risco de Viés (Aguardando Avaliação)", 
                          xaxis_title="Domínio", yaxis_title="Risco de Viés",
                          yaxis=dict(showticklabels=False), # Esconde ticks do eixo Y
                          xaxis=dict(categoryorder='array', categoryarray=[DOMAIN_NAMES[d] for d in DOMAIN_ORDER]))
        return fig

    # Prepara os dados para o gráfico
    data = []
    for domain_key in DOMAIN_ORDER:
        judgment = julgamentos.get(domain_key, PENDING)
        data.append({
            "Domínio": DOMAIN_NAMES.get(domain_key, domain_key),
            "Julgamento": judgment,
            "Cor": COLOR_MAP.get(judgment, COLOR_MAP[PENDING]),
            "Valor": 1 # Usamos um valor fixo para a altura da barra
        })
    
    df = pd.DataFrame(data)

    # Cria o gráfico de barras
    fig = go.Figure(go.Bar(
        x=df["Domínio"],
        y=df["Valor"],
        marker_color=df["Cor"],
        text=df["Julgamento"], # Mostra o julgamento na barra
        textposition="inside",
        insidetextanchor="middle",
        hoverinfo="x+text", # Mostra domínio e julgamento no hover
        width=0.6 # Largura das barras
    ))

    # Configurações do layout
    fig.update_layout(
        title="Risco de Viés por Domínio (RoB 2)",
        xaxis_title="", # Remover título do eixo x
        yaxis_title="", # Remover título do eixo y
        yaxis=dict(
            showticklabels=False, # Esconder labels do eixo y
            showgrid=False, # Esconder grid do eixo y
            range=[0, 1.2] # Ajustar range para dar espaço ao texto
        ),
        xaxis=dict(
            categoryorder='array', 
            categoryarray=[DOMAIN_NAMES[d] for d in DOMAIN_ORDER], # Garante a ordem correta
            tickangle=0 # Mantém os labels horizontais
        ),
        plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
        # uniformtext_minsize=8, 
        # uniformtext_mode='hide',
        height=300, # Altura do gráfico
        margin=dict(l=20, r=20, t=50, b=20) # Margens
    )
    
    # Ajusta a fonte do texto dentro das barras
    fig.update_traces(textfont_size=12, textfont_color='black')

    return fig


