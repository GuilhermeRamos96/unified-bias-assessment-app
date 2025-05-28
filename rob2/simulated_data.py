# utils/simulated_data.py

# Exemplos de respostas simuladas para testes

from .rob2_logic import YES, NO, NI, NA, LOW, SOME_CONCERNS, HIGH

SIMULATED_RESPONSES = {
    "Estudo Baixo Risco": {
        "study_info": {"id": "Estudo Exemplo 1 (Baixo Risco)", "outcome": "Mortalidade"},
        "responses": {
            "D1": {"1.1": YES[0], "1.2": YES[0], "1.3": NO[0]},
            "D2": {"2.1": NO[0], "2.2": NO[0], "2.3": NA, "2.4": NA, "2.5": YES[0], "2.6": NA},
            "D3": {"3.1": YES[0], "3.2": NA, "3.3": NA},
            "D4": {"4.1": NO[0], "4.2": NO[0], "4.3": YES[0], "4.4": NO[0]}, # Avaliador cego, desfecho objetivo
            "D5": {"5.1": YES[0], "5.2": NO[0], "5.3": NO[0]}
        },
        "expected_judgements": {
            "D1": LOW, "D2": LOW, "D3": LOW, "D4": LOW, "D5": LOW, "Geral": LOW
        }
    },
    "Estudo Alto Risco (Randomização)": {
        "study_info": {"id": "Estudo Exemplo 2 (Alto Risco)", "outcome": "Qualidade de Vida"},
        "responses": {
            "D1": {"1.1": NO[0], "1.2": NI, "1.3": YES[0]}, # Problemas claros na randomização
            "D2": {"2.1": YES[0], "2.2": YES[0], "2.3": NO[0], "2.4": NA, "2.5": YES[0], "2.6": NA}, # Não cego, mas sem desvios reportados
            "D3": {"3.1": YES[0], "3.2": NA, "3.3": NA},
            "D4": {"4.1": NO[0], "4.2": NO[0], "4.3": YES[0], "4.4": YES[0]}, # Não cego, desfecho subjetivo
            "D5": {"5.1": YES[0], "5.2": NO[0], "5.3": NO[0]}
        },
        "expected_judgements": {
            "D1": HIGH, "D2": SOME_CONCERNS, "D3": LOW, "D4": HIGH, "D5": LOW, "Geral": HIGH
        }
    },
    "Estudo Algumas Preocupações (Múltiplos Domínios)": {
        "study_info": {"id": "Estudo Exemplo 3 (Algumas Preocupações)", "outcome": "Dor (Escala VAS)"},
        "responses": {
            "D1": {"1.1": YES[0], "1.2": NI, "1.3": NO[0]}, # Ocultação não informada
            "D2": {"2.1": YES[0], "2.2": YES[0], "2.3": YES[0], "2.4": NI, "2.5": NO[0], "2.6": NI}, # Não cego, desvios, análise ITT não clara
            "D3": {"3.1": NO[0], "3.2": NO[0], "3.3": NI}, # Dados ausentes, sem análise robusta, razão incerta
            "D4": {"4.1": NO[0], "4.2": NO[0], "4.3": YES[0], "4.4": NI}, # Avaliador não cego, subjetivo, influência incerta
            "D5": {"5.1": NI, "5.2": YES[0], "5.3": NO[0]} # Plano não claro, seleção de medida
        },
        "expected_judgements": {
            "D1": SOME_CONCERNS, "D2": SOME_CONCERNS, "D3": SOME_CONCERNS, "D4": SOME_CONCERNS, "D5": SOME_CONCERNS, "Geral": HIGH # Múltiplas preocupações -> Alto Risco
        }
    }
}

def load_simulated_data(scenario_name, session_state):
    """Carrega dados simulados no session_state."""
    if scenario_name in SIMULATED_RESPONSES:
        data = SIMULATED_RESPONSES[scenario_name]
        session_state.study_info = data["study_info"].copy()
        session_state.responses = data["responses"].copy()
        # Limpa justificativas existentes para forçar a regeneração com base nos novos dados
        session_state.justifications = {}
        # Limpa resultados anteriores
        session_state.results = {
            "judgements": {key: PENDING for key in list(ROB2_QUESTIONS.keys()) + ["Geral"]},
            "table_data": pd.DataFrame(columns=["Domínio", "Julgamento", "Justificativa"])
        }
        # Define a seção atual para a visualização de resultados para ver o efeito
        session_state.current_section = "Resultados Consolidados"
        return True
    return False


