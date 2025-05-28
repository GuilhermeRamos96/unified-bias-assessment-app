# utils/simulated_data.py

# Dados simulados para teste da ferramenta ROBINS-I
# Estes são exemplos simplificados e podem não refletir perfeitamente
# a complexidade de estudos reais ou a interpretação oficial da ferramenta.

SIMULATED_RESPONSES_ROBINS_I = {
    "Cenário 1: Baixo Risco Simulado": {
        "study_info": {
            "id": "Simulado Baixo Risco", 
            "outcome": "Redução da Pressão Arterial", 
            "pico_p": "Adultos com hipertensão leve", 
            "pico_i": "Novo medicamento X", 
            "pico_c": "Placebo", 
            "pico_o": "Mudança na pressão arterial sistólica em 6 meses",
            "effect_interest": "Efeito da Designação"
        },
        "responses": {
            "D1": {"1.1": "Sim", "1.2": "Sim", "1.3": "Sim"},
            "D2": {"2.1": "Não", "2.3": "Sim", "2.4": "Não aplicável"}, # 2.2 e 2.4 dependem de 2.1
            "D3": {"3.1": "Sim", "3.2": "Sim", "3.3": "Não"},
            "D4": {"4.0_effect": "Efeito da Designação", "4.1_assignment": "Não", "4.2_assignment": "Não aplicável"}, # 4.2 depende de 4.1
            "D5": {"5.1": "Sim", "5.2": "Sim", "5.3": "Sim"}, # 5.4 depende de 5.3
            "D6": {"6.1": "Não", "6.2": "Não", "6.3": "Não"}, # 6.4 depende de 6.3
            "D7": {"7.1": "Não", "7.2": "Não", "7.3": "Não"}
        },
        "justifications": { # Justificativas simuladas
            "D1": "Controle adequado para idade, sexo e IMC via regressão.",
            "D2": "Seleção baseada em critérios pré-intervenção. Início do seguimento coincidiu com intervenção.",
            "D3": "Classificação baseada em registros de dispensação prévios ao desfecho.",
            "D4": "Protocolo seguido, sem desvios importantes reportados.",
            "D5": "Menos de 5% de dados faltantes, análise de sensibilidade não mostrou impacto.",
            "D6": "Mensuração objetiva (PA), avaliadores cegados.",
            "D7": "Protocolo pré-registrado com desfecho primário claro."
        }
    },
    "Cenário 2: Risco Sério Simulado": {
        "study_info": {
            "id": "Simulado Risco Sério", 
            "outcome": "Sobrevida em 5 anos", 
            "pico_p": "Pacientes com câncer avançado", 
            "pico_i": "Terapia Combinada", 
            "pico_c": "Monoterapia Padrão", 
            "pico_o": "Sobrevida global em 5 anos",
            "effect_interest": "Efeito da Aderência"
        },
        "responses": {
            "D1": {"1.1": "Provavelmente não", "1.2": "Sim", "1.3": "Não"}, # Falha no controle de confusão importante (estadiamento)
            "D2": {"2.1": "Não", "2.3": "Sim", "2.4": "Não aplicável"},
            "D3": {"3.1": "Sim", "3.2": "Sim", "3.3": "Não"},
            "D4": {"4.0_effect": "Efeito da Aderência", "4.1_adherence": "Sim", "4.2_adherence": "Não", "4.3_adherence": "Sim", "4.4_adherence": "Não"}, # Aderência desbalanceada, análise inadequada
            "D5": {"5.1": "Não", "5.2": "Não", "5.3": "Não", "5.4": "Provavelmente sim"}, # Muitos dados faltantes, provavelmente informativos
            "D6": {"6.1": "Não", "6.2": "Não", "6.3": "Sim", "6.4": "Provavelmente sim"}, # Avaliador ciente e pode ter influenciado
            "D7": {"7.1": "Não", "7.2": "Sim", "7.3": "Não"} # Seleção da análise
        },
         "justifications": {
            "D1": "Não controlou para estadiamento inicial da doença, um fator prognóstico chave.",
            "D2": "Seleção pré-intervenção.",
            "D3": "Classificação clara.",
            "D4": "Aderência muito menor no grupo de terapia combinada, análise ITT usada incorretamente para efeito da aderência.",
            "D5": "Mais de 30% de perda de seguimento, especialmente no grupo de intervenção, sem análise adequada.",
            "D6": "Avaliação da sobrevida feita por médico ciente da alocação, pode ter influenciado causa da morte.",
            "D7": "Múltiplos modelos estatísticos testados, apenas o mais favorável foi reportado."
        }
    }
}

def load_simulated_data_robins_i(scenario_name, session_state):
    """Carrega os dados de um cenário simulado no session_state."""
    scenario_data = SIMULATED_RESPONSES_ROBINS_I.get(scenario_name)
    if not scenario_data:
        return False
    
    try:
        # Carrega informações do estudo
        if "study_info" in scenario_data:
            for key, value in scenario_data["study_info"].items():
                session_state.study_info_robins_i[key] = value
        
        # Carrega respostas
        if "responses" in scenario_data:
            # Limpa respostas antigas antes de carregar novas
            session_state.responses_robins_i = {}
            for domain_key, domain_responses in scenario_data["responses"].items():
                session_state.responses_robins_i[domain_key] = domain_responses.copy()
                # Garante que a resposta para 4.0 esteja sincronizada com study_info
                if domain_key == "D4" and "effect_interest" in session_state.study_info_robins_i:
                     session_state.responses_robins_i["D4"]["4.0_effect"] = session_state.study_info_robins_i["effect_interest"]

        # Carrega justificativas
        if "justifications" in scenario_data:
             # Limpa justificativas antigas
             session_state.justifications_robins_i = {}
             for domain_key, justification in scenario_data["justifications"].items():
                 session_state.justifications_robins_i[domain_key] = justification
        else:
             session_state.justifications_robins_i = {} # Limpa se não houver no cenário

        # Limpa resultados antigos para forçar recálculo
        session_state.results_robins_i = {
            "judgements": {key: "Pendente" for key in list(SIMULATED_RESPONSES_ROBINS_I[scenario_name]["responses"].keys()) + ["Geral"]},
            "table_data": pd.DataFrame(columns=["Domínio", "Julgamento", "Justificativa"])
        }
        
        # Define a seção atual para a primeira página de domínio para visualização
        session_state.current_section_robins_i = "Informações do Estudo e Ensaio Alvo"
        
        return True
    except Exception as e:
        print(f"Erro ao carregar dados simulados ROBINS-I: {e}")
        return False

