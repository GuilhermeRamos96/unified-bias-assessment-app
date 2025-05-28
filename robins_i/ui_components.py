import streamlit as st
from .robins_i_logic import ROBINS_I_QUESTIONS, RESPONSE_OPTIONS

def render_domain_form_robins_i(domain_key, session_state):
    """Renderiza o formulário para um domínio ROBINS-I específico."""
    domain_info = ROBINS_I_QUESTIONS.get(domain_key)
    if not domain_info:
        st.error(f"Informações do domínio {domain_key} não encontradas.")
        return

    st.subheader(domain_info["name"])

    # Inicializa o dicionário de respostas para este domínio se não existir
    if domain_key not in session_state.responses:
        session_state.responses[domain_key] = {}

    # Renderiza cada pergunta sinalizadora
    for q_key, q_text in domain_info["questions"].items():
        # Define a chave única para o widget no session_state
        widget_key = f"response_{domain_key}_{q_key}"
        
        # Obtém a resposta atual do estado da sessão ou define como "Não selecionado"
        current_response = session_state.responses[domain_key].get(q_key, "Não selecionado")
        
        # Encontra o índice da resposta atual para o selectbox
        try:
            current_index = RESPONSE_OPTIONS.index(current_response)
        except ValueError:
            current_index = 0 # Default para "Não selecionado"

        # Cria o selectbox para a pergunta
        selected_response = st.selectbox(
            label=q_text,
            options=RESPONSE_OPTIONS,
            index=current_index,
            key=widget_key
        )
        
        # Atualiza o session_state se a resposta mudou
        if selected_response != current_response:
            session_state.responses[domain_key][q_key] = selected_response
            # st.rerun() # Pode ser necessário se houver lógica condicional complexa entre perguntas
        # Garante que a resposta esteja no estado mesmo que não mude
        elif q_key not in session_state.responses[domain_key]:
             session_state.responses[domain_key][q_key] = selected_response

    # Área para justificativa (será usada na seção de resultados)
    # justification_key = f"justification_{domain_key}"
    # if justification_key not in session_state.justifications:
    #     session_state.justifications[justification_key] = ""
    # st.text_area(
    #     label=domain_info["justification_label"],
    #     key=justification_key,
    #     height=100
    # )
    # session_state.justifications[domain_key] = st.session_state[justification_key]
    st.info("As justificativas serão preenchidas e editadas na seção 'Resultados Consolidados'.")


