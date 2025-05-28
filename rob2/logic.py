# rob2/logic.py
import streamlit as st # Import streamlit to access session state if needed indirectly

# Estrutura das perguntas (mantida para referência, mas a lógica usará as chaves)
ROB2_QUESTIONS = {
    "D1": {
        "name": "Domínio 1: Viés decorrente do processo de randomização",
        "questions": {
            "1.1": "1.1 A sequência de alocação foi aleatória?",
            "1.2": "1.2 A sequência de alocação foi ocultada até que os participantes fossem inscritos e designados para as intervenções?",
            "1.3": "1.3 As diferenças basais entre os grupos de intervenção sugeriram um problema com o processo de randomização?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 1"
    },
    "D2": {
        "name": "Domínio 2: Viés devido a desvios das intervenções pretendidas (Efeito da Designação - ITT)",
        "questions": {
            "2.1": "2.1 Os participantes sabiam qual intervenção lhes foi designada durante o ensaio?",
            "2.2": "2.2 Os cuidadores e as pessoas que administraram as intervenções sabiam qual intervenção foi designada aos participantes durante o ensaio?",
            "2.3": "2.3 (Se 2.1 ou 2.2 for Sim/Provavelmente Sim) Houve desvios da intervenção pretendida que surgiram devido ao contexto experimental?",
            "2.4": "2.4 (Se 2.3 for Sim/Provavelmente Sim) Esses desvios foram desequilibrados entre os grupos e provavelmente afetaram o desfecho?",
            "2.5": "2.5 Foi utilizada uma análise apropriada (por exemplo, ITT conforme definido no Capítulo 8) para estimar o efeito da designação para a intervenção?",
            "2.6": "2.6 (Se 2.5 for Não/Provavelmente Não) Se uma análise inadequada foi usada, o resultado provavelmente será substancialmente diferente do resultado de uma análise apropriada?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 2"
    },
    "D3": {
        "name": "Domínio 3: Viés devido a dados de desfecho ausentes",
        "questions": {
            "3.1": "3.1 Os dados para o desfecho estavam disponíveis para todos, ou quase todos, os participantes randomizados?",
            "3.2": "3.2 (Se Não/Provavelmente Não para 3.1) Há evidências de que o resultado não foi enviesado por dados de desfecho ausentes (por exemplo, análise de sensibilidade robusta)?",
            "3.3": "3.3 (Se Não/Provavelmente Não para 3.1) A ausência no desfecho poderia depender de seu valor verdadeiro?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 3"
    },
    "D4": {
        "name": "Domínio 4: Viés na mensuração do desfecho",
        "questions": {
            "4.1": "4.1 O método de mensuração do desfecho foi inadequado?",
            "4.2": "4.2 A mensuração ou apuração do desfecho poderia ter diferido entre os grupos de intervenção?",
            "4.3": "4.3 Os avaliadores do desfecho sabiam qual intervenção os participantes do estudo receberam?",
            "4.4": "4.4 (Se Sim/Provavelmente Sim para 4.3) A avaliação do desfecho poderia ter sido influenciada pelo conhecimento da intervenção recebida?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 4"
    },
    "D5": {
        "name": "Domínio 5: Viés na seleção do resultado relatado",
        "questions": {
            "5.1": "5.1 O ensaio foi analisado de acordo com um plano de análise pré-especificado que foi finalizado antes que os dados de desfecho não cegos estivessem disponíveis para análise?",
            "5.2": "5.2 O resultado numérico avaliado provavelmente foi selecionado, com base nos resultados, a partir de múltiplas mensurações de desfecho dentro do domínio do desfecho?",
            "5.3": "5.3 O resultado numérico avaliado provavelmente foi selecionado, com base nos resultados, a partir de múltiplas análises dos dados?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 5"
    }
}

RESPONSE_OPTIONS = ["Não selecionado", "Sim", "Provavelmente sim", "Provavelmente não", "Não", "Nenhuma informação", "Não aplicável"]
YES = ["Sim", "Provavelmente sim"]
NO = ["Não", "Provavelmente não"]
NI = "Nenhuma informação"
NA = "Não aplicável"
PENDING = "Pendente"
LOW = "Baixo risco de viés"
SOME_CONCERNS = "Algumas preocupações"
HIGH = "Alto risco de viés"

def check_pending(respostas, keys):
    """Verifica se alguma das respostas necessárias está pendente."""
    if not respostas or any(respostas.get(k) == "Não selecionado" for k in keys if respostas.get(k) != NA):
        return True
    return False

def avaliar_dominio_1(respostas_d1):
    keys = ["1.1", "1.2", "1.3"]
    if check_pending(respostas_d1, keys):
        return PENDING

    if respostas_d1.get("1.1") in NO or \
       respostas_d1.get("1.2") in NO or \
       respostas_d1.get("1.3") in YES:
        return HIGH
    
    if respostas_d1.get("1.1") == NI or \
       respostas_d1.get("1.2") == NI:
        return SOME_CONCERNS
        
    return LOW

def avaliar_dominio_2(respostas_d2):
    # Avalia D2 (Efeito da Designação - ITT)
    keys = ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"]
    if check_pending(respostas_d2, keys):
        return PENDING

    # Condições de Alto Risco
    cond1_high = (respostas_d2.get("2.1") in YES or respostas_d2.get("2.2") in YES) and \
                 respostas_d2.get("2.3") in YES and \
                 respostas_d2.get("2.4") in YES
    cond2_high = respostas_d2.get("2.5") in NO and respostas_d2.get("2.6") in YES

    if cond1_high or cond2_high:
        return HIGH

    # Condições de Algumas Preocupações
    cond1_some = (respostas_d2.get("2.1") in YES or respostas_d2.get("2.2") in YES) and \
                 respostas_d2.get("2.3") in YES and \
                 respostas_d2.get("2.4") in NO + [NI]
    cond2_some = respostas_d2.get("2.5") in NO and respostas_d2.get("2.6") in NO + [NI]
    cond3_some = any(respostas_d2.get(k) == NI for k in keys if respostas_d2.get(k) != NA)

    if cond1_some or cond2_some or cond3_some:
        return SOME_CONCERNS

    return LOW

def avaliar_dominio_3(respostas_d3):
    keys = ["3.1", "3.2", "3.3"]
    if check_pending(respostas_d3, keys):
        return PENDING

    # Condições de Baixo Risco
    if respostas_d3.get("3.1") in YES:
        return LOW
    if respostas_d3.get("3.1") in NO and respostas_d3.get("3.2") in YES:
         return LOW

    # Condições de Alto Risco
    if respostas_d3.get("3.1") in NO and \
       respostas_d3.get("3.2") in NO and \
       respostas_d3.get("3.3") in YES:
        return HIGH

    # Se chegou aqui, 3.1 é Não/Provavelmente Não. Qualquer outra combinação leva a Algumas Preocupações
    if respostas_d3.get("3.1") in NO:
        return SOME_CONCERNS
        
    # Fallback improvável, mas seguro
    return SOME_CONCERNS 

def avaliar_dominio_4(respostas_d4):
    keys = ["4.1", "4.2", "4.3", "4.4"]
    if check_pending(respostas_d4, keys):
        return PENDING

    # Condições de Alto Risco
    if respostas_d4.get("4.1") in YES or \
       respostas_d4.get("4.2") in YES:
        return HIGH
    if respostas_d4.get("4.3") in YES and respostas_d4.get("4.4") in YES:
        return HIGH

    # Condições de Algumas Preocupações
    if respostas_d4.get("4.3") in YES and respostas_d4.get("4.4") in NO + [NI]:
        return SOME_CONCERNS
    if any(respostas_d4.get(k) == NI for k in keys if respostas_d4.get(k) != NA):
         return SOME_CONCERNS

    return LOW

def avaliar_dominio_5(respostas_d5):
    keys = ["5.1", "5.2", "5.3"]
    if check_pending(respostas_d5, keys):
        return PENDING

    # Condições de Alto Risco
    if respostas_d5.get("5.1") in NO and \
       (respostas_d5.get("5.2") in YES or respostas_d5.get("5.3") in YES):
        return HIGH

    # Condições de Algumas Preocupações
    cond1_some = respostas_d5.get("5.1") in NO and \
                 respostas_d5.get("5.2") in NO + [NI] and \
                 respostas_d5.get("5.3") in NO + [NI]
    cond2_some = respostas_d5.get("5.1") in YES and \
                 (respostas_d5.get("5.2") in YES or respostas_d5.get("5.3") in YES)
    cond3_some = any(respostas_d5.get(k) == NI for k in keys)

    if cond1_some or cond2_some or cond3_some:
        return SOME_CONCERNS

    return LOW

def avaliar_rob2_geral(julgamentos_dominios):
    """Avalia o risco de viés geral com base nos julgamentos dos domínios."""
    if not julgamentos_dominios or any(j == PENDING for j in julgamentos_dominios.values()):
        return PENDING
    
    if any(j == HIGH for j in julgamentos_dominios.values()):
        return HIGH
    
    # Contar 'Algumas Preocupações'
    some_concerns_count = sum(1 for j in julgamentos_dominios.values() if j == SOME_CONCERNS)
    
    # Regra: Múltiplas 'Algumas Preocupações' podem levar a 'Alto Risco' (ajustar critério se necessário)
    # Aqui, consideramos >= 3 como 'múltiplas' para exemplo, mas pode ser ajustado
    if some_concerns_count >= 3: # Critério de exemplo para 'múltiplas preocupações' -> Alto Risco
         # st.warning("Julgamento geral definido como Alto Risco devido a múltiplas preocupações em domínios.") # Feedback opcional
         return HIGH 
            
    if some_concerns_count > 0:
        return SOME_CONCERNS
        
    return LOW

def gerar_justificativa_sugerida(domain_key, respostas):
    """Gera um texto inicial para a justificativa com base nas respostas."""
    sugestao = f"Avaliação do {ROB2_QUESTIONS[domain_key]['name']}:\n"
    if respostas:
        for q_key, answer in respostas.items():
            if answer != NA and answer != "Não selecionado":
                question_text = ROB2_QUESTIONS[domain_key]['questions'].get(q_key, q_key)
                # Remove o prefixo numérico para ficar mais legível
                question_text_clean = ".".join(question_text.split(".")[1:]).strip()
                if question_text_clean:
                    sugestao += f"- {question_text_clean}: {answer}\n"
    else:
        sugestao += "Nenhuma resposta fornecida ainda.\n"
    return sugestao

# Função principal para orquestrar a avaliação (chamada pelo app.py)
def run_rob2_assessment(responses):
    """Executa a avaliação para todos os domínios e o geral."""
    julgamentos = {}
    avaliadores = {
        "D1": avaliar_dominio_1,
        "D2": avaliar_dominio_2,
        "D3": avaliar_dominio_3,
        "D4": avaliar_dominio_4,
        "D5": avaliar_dominio_5
    }
    
    all_domains_answered = True
    for d_key in ROB2_QUESTIONS.keys():
        domain_responses = responses.get(d_key, {})
        julgamentos[d_key] = avaliadores[d_key](domain_responses)
        if julgamentos[d_key] == PENDING:
            all_domains_answered = False
            
    if all_domains_answered:
        julgamentos["Geral"] = avaliar_rob2_geral({k: v for k, v in julgamentos.items() if k != "Geral"})
    else:
        julgamentos["Geral"] = PENDING
        
    return julgamentos


