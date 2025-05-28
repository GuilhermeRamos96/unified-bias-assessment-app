# utils/ui_components.py
import streamlit as st
from .rob2_logic import ROB2_QUESTIONS, RESPONSE_OPTIONS

def render_domain_form(domain_key, session_state):
    """Renderiza o formulário para um domínio RoB 2 específico."""
    domain_info = ROB2_QUESTIONS[domain_key]
    st.subheader(domain_info["name"])

    # Inicializa as respostas para este domínio no session_state se não existirem
    if domain_key not in session_state.responses:
        session_state.responses[domain_key] = {q_key: RESPONSE_OPTIONS[0] for q_key in domain_info["questions"]}
    if domain_key not in session_state.justifications:
        session_state.justifications[domain_key] = ""

    # Exibe as perguntas sinalizadoras
    for q_key, q_text in domain_info["questions"].items():
        # Lógica simples para perguntas condicionais (pode precisar ser mais robusta)
        show_question = True
        if q_key == "2.3" and session_state.responses["D2"].get("2.1", "Não selecionado") in ["Não", "Provavelmente não", "Não selecionado"] and session_state.responses["D2"].get("2.2", "Não selecionado") in ["Não", "Provavelmente não", "Não selecionado"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável" # Define como N/A se condição não atendida
        elif q_key == "2.4" and session_state.responses["D2"].get("2.3", "Não selecionado") in ["Não", "Provavelmente não", "Não selecionado", "Não aplicável"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável"
        elif q_key == "2.6" and session_state.responses["D2"].get("2.5", "Não selecionado") in ["Sim", "Provavelmente sim", "Não selecionado"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável"
        elif q_key == "3.2" and session_state.responses["D3"].get("3.1", "Não selecionado") in ["Sim", "Provavelmente sim", "Não selecionado"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável"
        elif q_key == "3.3" and session_state.responses["D3"].get("3.1", "Não selecionado") in ["Sim", "Provavelmente sim", "Não selecionado"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável"
        elif q_key == "4.4" and session_state.responses["D4"].get("4.3", "Não selecionado") in ["Não", "Provavelmente não", "Não selecionado"]:
            show_question = False
            session_state.responses[domain_key][q_key] = "Não aplicável"
        # Adicionar outras lógicas condicionais conforme necessário
        
        # Garante que a chave exista antes de tentar acessá-la
        current_value = session_state.responses[domain_key].get(q_key, RESPONSE_OPTIONS[0])
        # Garante que o valor atual esteja nas opções válidas
        current_index = RESPONSE_OPTIONS.index(current_value) if current_value in RESPONSE_OPTIONS else 0

        if show_question:
            # Usa a chave completa (domínio + pergunta) para garantir unicidade no Streamlit
            widget_key = f"{domain_key}_{q_key}"
            session_state.responses[domain_key][q_key] = st.radio(
                q_text,
                options=RESPONSE_OPTIONS,
                index=current_index,
                key=widget_key,
                horizontal=True,
            )
        elif q_key in session_state.responses[domain_key] and session_state.responses[domain_key][q_key] != "Não aplicável":
             # Se a pergunta ficou oculta, mas tinha uma resposta anterior diferente de N/A, reseta para N/A
             session_state.responses[domain_key][q_key] = "Não aplicável"

    st.divider()
    # Campo para justificativa
    session_state.justifications[domain_key] = st.text_area(
        domain_info["justification_label"],
        value=session_state.justifications.get(domain_key, ""),
        height=150,
        key=f"just_{domain_key}"
    )

    # Debug: Exibe as respostas atuais para este domínio
    # st.write("Debug - Respostas:", session_state.responses[domain_key])
    # st.write("Debug - Justificativa:", session_state.justifications[domain_key])

