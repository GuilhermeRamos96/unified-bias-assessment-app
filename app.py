import streamlit as st
import pandas as pd
import os

# Importar utilitários comuns
from utils.pdf_handler import display_pdf
from utils.export_utils import exportar_para_csv, exportar_para_pdf

# Importar módulos específicos (serão chamados dinamicamente)
# RoB 2
from rob2.logic import ROB2_QUESTIONS, run_rob2_assessment, gerar_justificativa_sugerida_rob2, PENDING as PENDING_ROB2
from rob2.ui_components import render_domain_form_rob2
from rob2.plotting import criar_grafico_semaforo_rob2, ROB2_DOMAIN_ORDER, ROB2_DOMAIN_NAMES
from rob2.simulated_data import SIMULATED_RESPONSES_ROB2, load_simulated_data_rob2
from rob2.export import gerar_html_relatorio_rob2 # Função específica de exportação RoB2

# ROBINS-I
from robins_i.logic import ROBINS_I_QUESTIONS, run_robins_i_assessment, gerar_justificativa_sugerida_robins_i, PENDING as PENDING_ROBINS_I
from robins_i.ui_components import render_domain_form_robins_i
from robins_i.plotting import criar_grafico_semaforo_robins_i, ROBINS_I_DOMAIN_ORDER, ROBINS_I_DOMAIN_NAMES
from robins_i.simulated_data import SIMULATED_RESPONSES_ROBINS_I, load_simulated_data_robins_i
from robins_i.export import gerar_html_relatorio_robins_i # Função específica de exportação ROBINS-I

# Configuração inicial da página
st.set_page_config(layout="wide", page_title="Análise de Risco de Viés")

# --- Inicialização do Session State --- 
def initialize_state():
    # Estado global
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = "RoB 2" # Default para RoB 2
    if "uploaded_pdf" not in st.session_state:
        st.session_state.uploaded_pdf = None
    if "current_section" not in st.session_state:
        st.session_state.current_section = "Introdução / Visualizar Estudo"

    # Estado específico para RoB 2
    if "rob2_state" not in st.session_state:
        st.session_state.rob2_state = {
            "study_info": {"id": "", "outcome": ""},
            "responses": {},
            "justifications": {},
            "results": {
                "judgements": {key: PENDING_ROB2 for key in list(ROB2_QUESTIONS.keys()) + ["Geral"]},
                "table_data": pd.DataFrame(columns=["Domínio", "Julgamento", "Justificativa"])
            },
            "selected_simulation": list(SIMULATED_RESPONSES_ROB2.keys())[0] if SIMULATED_RESPONSES_ROB2 else None
        }

    # Estado específico para ROBINS-I
    if "robins_i_state" not in st.session_state:
        st.session_state.robins_i_state = {
            "study_info": {"id": "", "outcome": "", "pico_p": "", "pico_i": "", "pico_c": "", "pico_o": "", "effect_interest": "Efeito da Designação"},
            "responses": {},
            "justifications": {},
            "results": {
                "judgements": {key: PENDING_ROBINS_I for key in list(ROBINS_I_QUESTIONS.keys()) + ["Geral"]},
                "table_data": pd.DataFrame(columns=["Domínio", "Julgamento", "Justificativa"])
            },
            "selected_simulation": list(SIMULATED_RESPONSES_ROBINS_I.keys())[0] if SIMULATED_RESPONSES_ROBINS_I else None
        }

initialize_state()

# Determina o estado ativo com base na ferramenta selecionada
active_state = st.session_state.rob2_state if st.session_state.selected_tool == "RoB 2" else st.session_state.robins_i_state

# --- Barra Lateral ---
with st.sidebar:
    st.title("Análise de Risco de Viés")

    # Seletor de Ferramenta
    selected_tool_sidebar = st.radio(
        "Escolha a Ferramenta:",
        options=["RoB 2", "ROBINS-I"],
        key="tool_selector",
        horizontal=True,
        index=0 if st.session_state.selected_tool == "RoB 2" else 1
    )
    # Se a ferramenta mudou, atualiza o estado e reseta a seção para Introdução
    if selected_tool_sidebar != st.session_state.selected_tool:
        st.session_state.selected_tool = selected_tool_sidebar
        st.session_state.current_section = "Introdução / Visualizar Estudo"
        st.rerun() # Força o rerender com a nova ferramenta
        
    st.caption(f"Analisando com: {st.session_state.selected_tool}")
    st.divider()

    # Upload do PDF (comum)
    uploaded_file = st.file_uploader("Carregar Estudo (PDF)", type="pdf", key="pdf_uploader")
    if uploaded_file:
        if st.session_state.uploaded_pdf is None or uploaded_file.id != st.session_state.uploaded_pdf.id:
             st.session_state.uploaded_pdf = uploaded_file
    elif "uploaded_pdf" in st.session_state and st.session_state.uploaded_pdf is not None:
        uploaded_file = st.session_state.uploaded_pdf
        st.info(f"Arquivo: {uploaded_file.name}")
        if st.button("Remover PDF", key="remove_pdf"):
            st.session_state.uploaded_pdf = None
            st.rerun()

    st.divider()

    # Navegação Dinâmica
    if st.session_state.selected_tool == "RoB 2":
        navigation_options = [
            "Introdução / Visualizar Estudo",
            "Informações do Estudo (RoB 2)",
            "Domínio 1: Randomização",
            "Domínio 2: Desvios Intervenções",
            "Domínio 3: Dados Ausentes",
            "Domínio 4: Mensuração Desfecho",
            "Domínio 5: Seleção Relato",
            "Resultados Consolidados (RoB 2)",
            "Exportar Relatório (RoB 2)"
        ]
        sim_options = SIMULATED_RESPONSES_ROB2
        load_sim_func = load_simulated_data_rob2
        sim_key = "rob2_sim_select"
        load_key = "load_rob2_sim"
    else: # ROBINS-I
        navigation_options = [
            "Introdução / Visualizar Estudo",
            "Informações do Estudo e Ensaio Alvo (ROBINS-I)",
            "Domínio 1: Confusão",
            "Domínio 2: Seleção Participantes",
            "Domínio 3: Classificação Intervenções",
            "Domínio 4: Desvios Intervenções",
            "Domínio 5: Dados Faltantes",
            "Domínio 6: Mensuração Desfechos",
            "Domínio 7: Seleção Relato",
            "Resultados Consolidados (ROBINS-I)",
            "Exportar Relatório (ROBINS-I)"
        ]
        sim_options = SIMULATED_RESPONSES_ROBINS_I
        load_sim_func = load_simulated_data_robins_i
        sim_key = "robins_i_sim_select"
        load_key = "load_robins_i_sim"

    try:
        current_index = navigation_options.index(st.session_state.current_section)
    except ValueError:
        # Se a seção atual não existe na nova lista (mudou de ferramenta), volta para Introdução
        current_index = 0
        st.session_state.current_section = navigation_options[0]
        
    st.session_state.current_section = st.radio(
        "Navegar para:",
        options=navigation_options,
        key="navigation_radio",
        index=current_index
    )

    st.divider()
    # --- Carregar Dados Simulados (Dinâmico) ---
    st.subheader(f"Testar {st.session_state.selected_tool} com Dados Simulados")
    sim_keys = list(sim_options.keys()) if sim_options else []
    if sim_keys:
        # Usa a chave específica da ferramenta para o selectbox
        # Garante que a chave de simulação exista no estado ativo
        if "selected_simulation" not in active_state:
             active_state["selected_simulation"] = sim_keys[0] if sim_keys else None
             
        sim_scenario = st.selectbox(
            "Escolha um cenário:", 
            options=sim_keys,
            key=sim_key,
            index=sim_keys.index(active_state["selected_simulation"]) if active_state["selected_simulation"] in sim_keys else 0
        )
        # Atualiza a simulação selecionada no estado ativo
        active_state["selected_simulation"] = sim_scenario 
        
        if st.button(f"Carregar Cenário Simulado {st.session_state.selected_tool}", key=load_key):
            # Passa o estado ativo para a função de carregamento
            if load_sim_func(sim_scenario, active_state):
                st.success(f"Cenário \'{sim_scenario}\' carregado para {st.session_state.selected_tool}.\")
                # Resetar a seção atual para a introdução ou info do estudo após carregar
                st.session_state.current_section = navigation_options[1] # Vai para Info Estudo
                st.rerun()
            else:
                st.error("Falha ao carregar cenário.")
    else:
        st.caption(f"Nenhum cenário simulado disponível para {st.session_state.selected_tool}.\")

# --- Área Principal (Conteúdo Dinâmico) ---
st.header(st.session_state.current_section)

# --- Lógica para renderizar conteúdo baseado na seção e ferramenta --- 

if st.session_state.current_section == "Introdução / Visualizar Estudo":
    st.markdown(f"""
    Bem-vindo à ferramenta de Análise de Risco de Viés.
    
    Ferramenta selecionada: **{st.session_state.selected_tool}**
    
    Use a barra lateral para:
    1.  Selecionar a ferramenta desejada (RoB 2 para ensaios randomizados, ROBINS-I para não randomizados).
    2.  **(Opcional)** Carregar o estudo em PDF.
    3.  Navegar pelas seções para inserir informações e responder às perguntas.
    4.  **(Opcional)** Carregar dados simulados para teste.
    5.  Visualizar e exportar os resultados.
    """)
    st.divider()
    display_pdf(st.session_state.uploaded_pdf)

elif st.session_state.current_section.startswith("Informações do Estudo"):
    if st.session_state.selected_tool == "RoB 2":
        st.subheader("Detalhes do Estudo (RoB 2)")
        active_state["study_info"]["id"] = st.text_input("Identificador do Estudo (ex: Autor Ano)", value=active_state["study_info"].get("id",""), key="rob2_study_id")
        active_state["study_info"]["outcome"] = st.text_input("Desfecho(s) Específico(s) Sendo Avaliado(s)", value=active_state["study_info"].get("outcome",""), key="rob2_study_outcome")
    else: # ROBINS-I
        st.subheader("Detalhes do Estudo Não Randomizado Avaliado")
        active_state["study_info"]["id"] = st.text_input("Identificador do Estudo (ex: Autor Ano)", value=active_state["study_info"].get("id",""), key="robins_study_id")
        active_state["study_info"]["outcome"] = st.text_input("Desfecho(s) Específico(s) Sendo Avaliado(s)", value=active_state["study_info"].get("outcome",""), key="robins_study_outcome")
        st.divider()
        st.subheader("Descrição do Ensaio Clínico Randomizado Alvo (Target Trial)")
        col1, col2 = st.columns(2)
        with col1:
            active_state["study_info"]["pico_p"] = st.text_area("População (P)", value=active_state["study_info"].get("pico_p",""), key="robins_pico_p")
            active_state["study_info"]["pico_i"] = st.text_area("Intervenção (I)", value=active_state["study_info"].get("pico_i",""), key="robins_pico_i")
        with col2:
            active_state["study_info"]["pico_c"] = st.text_area("Comparador (C)", value=active_state["study_info"].get("pico_c",""), key="robins_pico_c")
            active_state["study_info"]["pico_o"] = st.text_area("Desfecho (O)", value=active_state["study_info"].get("pico_o",""), key="robins_pico_o")
        active_state["study_info"]["effect_interest"] = st.radio("Efeito de Interesse Principal:", options=["Efeito da Designação", "Efeito da Aderência"], index=0 if active_state["study_info"].get("effect_interest", "Efeito da Designação") == "Efeito da Designação" else 1, key="robins_effect_interest", horizontal=True)
        # Atualiza D4.0 na resposta
        if "D4" not in active_state["responses"]:
             active_state["responses"]["D4"] = {}
        active_state["responses"]["D4"]["4.0_effect"] = active_state["study_info"].get("effect_interest", "Efeito da Designação")

elif st.session_state.current_section.startswith("Domínio"):
    # Extrai o número do domínio e chama a função de renderização correta
    try:
        domain_part = st.session_state.current_section.split(":")[0]
        domain_num = domain_part.split(" ")[-1]
        domain_key = f"D{domain_num}"
        if st.session_state.selected_tool == "RoB 2":
            if domain_key in ROB2_QUESTIONS:
                render_domain_form_rob2(domain_key, active_state) # Passa o estado RoB 2
            else:
                st.error(f"Domínio RoB 2 {domain_key} não encontrado.")
        else: # ROBINS-I
            if domain_key in ROBINS_I_QUESTIONS:
                render_domain_form_robins_i(domain_key, active_state) # Passa o estado ROBINS-I
            else:
                st.error(f"Domínio ROBINS-I {domain_key} não encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar formulário do domínio: {e}")

elif st.session_state.current_section.startswith("Resultados Consolidados"):
    st.subheader(f"Resumo da Avaliação {st.session_state.selected_tool}")
    
    # Determina qual conjunto de funções e dados usar
    if st.session_state.selected_tool == "RoB 2":
        run_assessment_func = run_rob2_assessment
        create_plot_func = criar_grafico_semaforo_rob2
        domain_order = ROB2_DOMAIN_ORDER
        domain_names = ROB2_DOMAIN_NAMES
        gen_justif_func = gerar_justificativa_sugerida_rob2
        pending_val = PENDING_ROB2
        questions = ROB2_QUESTIONS
    else: # ROBINS-I
        run_assessment_func = run_robins_i_assessment
        create_plot_func = criar_grafico_semaforo_robins_i
        domain_order = ROBINS_I_DOMAIN_ORDER
        domain_names = ROBINS_I_DOMAIN_NAMES
        gen_justif_func = gerar_justificativa_sugerida_robins_i
        pending_val = PENDING_ROBINS_I
        questions = ROBINS_I_QUESTIONS

    # Executa a avaliação e atualiza o estado
    judgements = run_assessment_func(active_state["responses"])
    active_state["results"]["judgements"] = judgements
    
    # Mostra o gráfico
    st.plotly_chart(create_plot_func(judgements), use_container_width=True)
    st.divider()
    
    # Prepara e mostra a tabela de resultados editável
    st.subheader("Julgamentos e Justificativas por Domínio")
    table_rows = []
    all_domains_judged = True
    for d_key in domain_order:
        domain_name = domain_names.get(d_key, d_key)
        judgment = judgements.get(d_key, pending_val)
        if judgment == pending_val:
             all_domains_judged = False
             
        # Gera sugestão se a justificativa estiver vazia e o domínio não for Geral
        if d_key != "Geral" and not active_state["justifications"].get(d_key):
             suggested_justification = gen_justif_func(d_key, active_state["responses"].get(d_key, {}))
             active_state["justifications"][d_key] = suggested_justification
             
        justification = active_state["justifications"].get(d_key, "-") if d_key != "Geral" else "(Julgamento geral baseado nos domínios)"
        table_rows.append({
            "Domínio": domain_name,
            "Julgamento": judgment,
            "Justificativa": justification
        })
        
    df_results = pd.DataFrame(table_rows)
    column_config = {
        "Domínio": st.column_config.TextColumn("Domínio", disabled=True, width="medium"),
        "Julgamento": st.column_config.TextColumn("Julgamento", disabled=True, width="small"),
        "Justificativa": st.column_config.TextColumn("Justificativa (Editável)", width="large")
    }
    
    editor_key = f"results_editor_{st.session_state.selected_tool.lower().replace(' ','_')}"
    
    if all_domains_judged:
        edited_df = st.data_editor(
            df_results,
            column_config=column_config,
            num_rows="fixed",
            key=editor_key,
            hide_index=True,
            use_container_width=True
        )
        # Atualiza as justificativas no estado se o dataframe foi editado
        if not edited_df.equals(df_results):
            for index, row in edited_df.iterrows():
                domain_name = row["Domínio"]
                # Encontra a chave do domínio (D1, D2, etc.) pelo nome
                domain_key = next((dk for dk, dn in domain_names.items() if dn == domain_name), None)
                if domain_key and domain_key != "Geral":
                    active_state["justifications"][domain_key] = row["Justificativa"]
            active_state["results"]["table_data"] = edited_df # Salva o DF editado
            # st.rerun() # Pode ser útil para refletir mudanças imediatamente, mas pode atrapalhar edição longa
        else:
             active_state["results"]["table_data"] = df_results # Salva o DF original se não houve edição
    else:
        st.warning("Responda às perguntas de todos os domínios para habilitar a edição das justificativas e a exportação.")
        st.dataframe(df_results, hide_index=True, use_container_width=True)
        active_state["results"]["table_data"] = df_results # Salva o DF mesmo não editável

    if st.button(f"Atualizar Avaliação e Gráfico ({st.session_state.selected_tool})", key=f"update_results_{st.session_state.selected_tool.lower()}"):
        st.rerun()

elif st.session_state.current_section.startswith("Exportar Relatório"):
    st.subheader(f"Exportar Resultados da Análise {st.session_state.selected_tool}")
    
    # Determina qual conjunto de dados e funções usar
    if st.session_state.selected_tool == "RoB 2":
        judgements_export = active_state["results"].get("judgements", {})
        df_export = active_state["results"].get("table_data", pd.DataFrame())
        gen_html_func = gerar_html_relatorio_rob2
        pending_val = PENDING_ROB2
        tool_prefix = "rob2"
    else: # ROBINS-I
        judgements_export = active_state["results"].get("judgements", {})
        df_export = active_state["results"].get("table_data", pd.DataFrame())
        gen_html_func = gerar_html_relatorio_robins_i
        pending_val = PENDING_ROBINS_I
        tool_prefix = "robins_i"
        
    is_complete_export = all(j != pending_val for j in judgements_export.values()) and not df_export.empty

    if is_complete_export:
        st.success(f"A avaliação {st.session_state.selected_tool} está completa. Você pode exportar os resultados.")
        study_id_filename = active_state["study_info"].get("id", "estudo").replace(" ", "_").replace("/", "-")
        
        # Exportar CSV
        csv_data = exportar_para_csv(df_export)
        if csv_data:
            st.download_button(
                label="Baixar Resultados em CSV",
                data=csv_data,
                file_name=f"{tool_prefix}_analise_{study_id_filename}.csv",
                mime="text/csv",
                key=f"download_csv_{tool_prefix}"
            )
        else:
            st.error("Falha ao gerar o arquivo CSV.")

        # Exportar PDF
        # Passa study_info e df_export para a função específica de geração de HTML
        html_report = gen_html_func(active_state["study_info"], df_export)
        if html_report:
            pdf_data = exportar_para_pdf(html_report)
            if pdf_data:
                st.download_button(
                    label="Baixar Relatório em PDF",
                    data=pdf_data,
                    file_name=f"{tool_prefix}_relatorio_{study_id_filename}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_{tool_prefix}"
                )
            else:
                st.error("Falha ao gerar o arquivo PDF.")
        else:
             st.error("Falha ao gerar o conteúdo HTML para o PDF.")

        st.divider()
        st.subheader("Dados para Exportação:")
        st.dataframe(df_export, hide_index=True, use_container_width=True)

    else:
        st.warning(f"A avaliação {st.session_state.selected_tool} ainda não está completa. Por favor, revise as respostas em todos os domínios na seção 'Resultados Consolidados'.")
        # Mostra a tabela mesmo incompleta para referência
        if not df_export.empty:
             st.dataframe(df_export, hide_index=True, use_container_width=True)
        else:
             st.info("Nenhum resultado para exibir ainda. Complete a avaliação.")

# --- Rodapé ---
st.divider()
st.caption(f"Usando: {st.session_state.selected_tool} | Baseado nos Capítulos 8 e 25 do Cochrane Handbook")

# Debug: Mostrar estado da sessão
# with st.expander("Debug: Session State"):
#     st.json({k: v for k, v in st.session_state.items()})

