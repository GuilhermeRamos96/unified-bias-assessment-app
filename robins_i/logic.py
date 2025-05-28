# robins_i/logic.py

# Nota: As perguntas exatas e algoritmos detalhados devem ser verificados
# em www.riskofbias.info conforme indicado no Capítulo 25.
# Esta estrutura e lógica são baseadas nos resumos do capítulo.

# Opções de resposta padrão
RESPONSE_OPTIONS = ["Não selecionado", "Sim", "Provavelmente sim", "Provavelmente não", "Não", "Nenhuma informação"]
YES = ["Sim", "Provavelmente sim"]
NO = ["Não", "Provavelmente não"]
NI = "Nenhuma informação"

# Níveis de Julgamento ROBINS-I
LOW = "Baixo risco de viés"
MODERATE = "Risco moderado de viés"
SERIOUS = "Risco sério de viés"
CRITICAL = "Risco crítico de viés"
NO_INFO = "Nenhuma informação"
PENDING = "Pendente"

# Estrutura das Perguntas (Baseada nos resumos das Tabelas 25.4.a, 25.5.a, 25.6.a)
# As chaves (e.g., D1.1) são placeholders.
ROBINS_I_QUESTIONS = {
    "D1": {
        "name": "Domínio 1: Viés devido à confusão (Confounding)",
        "questions": {
            "1.1": "1.1 O estudo controlou para todos os domínios de confusão importantes (baseline e/ou variáveis no tempo)?",
            "1.2": "1.2 Os domínios de confusão foram medidos de forma válida e confiável?",
            "1.3": "1.3 Foram usados métodos de análise apropriados para controlar a confusão?",
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 1"
    },
    "D2": {
        "name": "Domínio 2: Viés na seleção de participantes",
        "questions": {
            "2.1": "2.1 A seleção de participantes (ou para a análise) foi baseada em características pós-início da intervenção?",
            "2.2": "2.2 (Se Sim/Provavelmente Sim para 2.1) Essas características estavam associadas à intervenção E influenciadas pelo desfecho (ou causa do desfecho)?",
            "2.3": "2.3 O início do seguimento e o início da intervenção foram os mesmos (sem viés de inception)?",
            "2.4": "2.4 Foram usadas técnicas de ajuste apropriadas para corrigir vieses de seleção (se presentes)?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 2"
    },
    "D3": {
        "name": "Domínio 3: Viés na classificação das intervenções",
        "questions": {
            "3.1": "3.1 O status da intervenção foi classificado corretamente para (quase) todos os participantes?",
            "3.2": "3.2 A informação usada para classificar a intervenção foi registrada no início da intervenção (ou antes)?",
            "3.3": "3.3 A classificação da intervenção poderia ter sido influenciada pelo conhecimento do desfecho ou risco do desfecho?",
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 3"
    },
    "D4": {
        "name": "Domínio 4: Viés devido a desvios das intervenções pretendidas",
        "questions": {
            # Perguntas variam MUITO dependendo do efeito de interesse (Designação vs Aderência)
            # O app precisará perguntar o efeito de interesse primeiro.
            # Aqui, incluímos todas como exemplo, mas a lógica precisará ser condicional.
            "4.0_effect": "4.0 Qual o efeito de interesse principal? (Efeito da Designação / Efeito da Aderência)", # Pergunta adicional
            "4.1_assignment": "4.1 (Efeito da Designação) Houve desvios da intervenção pretendida devido ao contexto experimental?",
            "4.2_assignment": "4.2 (Efeito da Designação - Se 4.1 Sim) Esses desvios foram desbalanceados e provavelmente afetaram o desfecho?",
            "4.1_adherence": "4.1 (Efeito da Aderência) Cointervenções importantes foram balanceadas entre os grupos?",
            "4.2_adherence": "4.2 (Efeito da Aderência) Falhas na implementação afetaram o desfecho e foram desbalanceadas?",
            "4.3_adherence": "4.3 (Efeito da Aderência) A aderência foi desbalanceada entre os grupos?",
            "4.4_adherence": "4.4 (Efeito da Aderência) Foi usada análise apropriada para estimar o efeito da aderência?",
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 4"
    },
    "D5": {
        "name": "Domínio 5: Viés devido a dados faltantes",
        "questions": {
            "5.1": "5.1 A proporção de participantes omitidos por dados faltantes do desfecho foi pequena?",
            "5.2": "5.2 A proporção de participantes omitidos por dados faltantes da intervenção ou outras variáveis foi pequena?",
            "5.3": "5.3 Há evidência de que o resultado NÃO foi enviesado pelos dados faltantes (ex: análise de sensibilidade robusta)?",
            "5.4": "5.4 (Se Não/Provavelmente Não para 5.3) A falta de dados do desfecho provavelmente dependia do valor verdadeiro do desfecho?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 5"
    },
    "D6": {
        "name": "Domínio 6: Viés na mensuração dos desfechos",
        "questions": {
            "6.1": "6.1 O método de mensuração do desfecho foi inadequado?",
            "6.2": "6.2 A mensuração ou apuração do desfecho poderia ter diferido entre os grupos de intervenção?",
            "6.3": "6.3 Os avaliadores do desfecho sabiam qual intervenção os participantes receberam?",
            "6.4": "6.4 (Se Sim/Provavelmente Sim para 6.3) A avaliação do desfecho poderia ter sido influenciada pelo conhecimento da intervenção recebida?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 6"
    },
    "D7": {
        "name": "Domínio 7: Viés na seleção do resultado relatado",
        "questions": {
            "7.1": "7.1 O resultado numérico avaliado provavelmente foi selecionado (com base nos resultados) a partir de múltiplas mensurações do desfecho dentro do domínio do desfecho?",
            "7.2": "7.2 O resultado numérico avaliado provavelmente foi selecionado (com base nos resultados) a partir de múltiplas análises dos dados?",
            "7.3": "7.3 O resultado numérico avaliado provavelmente foi selecionado (com base nos resultados) a partir de múltiplos subgrupos?"
        },
        "justification_label": "Justificativa de suporte para o julgamento do Domínio 7"
    }
}

# Funções de avaliação (Lógica simplificada baseada nos resumos - REQUER REFINAMENTO)
def check_pending_robins(respostas, keys):
    if not respostas:
        return True
    # Verifica se todas as chaves relevantes têm uma resposta válida
    for k in keys:
        # Ignora chaves condicionais que não se aplicam (ex: 2.2 se 2.1 for Não)
        # Esta lógica condicional precisa ser implementada aqui ou na função de avaliação
        if respostas.get(k, "Não selecionado") == "Não selecionado":
            return True
    return False

def avaliar_dominio_1_robins(respostas_d1):
    keys = ["1.1", "1.2", "1.3"]
    if check_pending_robins(respostas_d1, keys): return PENDING

    if respostas_d1.get("1.1") in NO or respostas_d1.get("1.3") in NO:
        # Falha no controle ou método inadequado -> Sério/Crítico
        # A distinção entre Sério e Crítico depende da importância/magnitude da falha (não capturado aqui)
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d1.get("1.2") in NO:
        # Medição inválida/não confiável -> Sério
        return SERIOUS
    if any(respostas_d1.get(k) == NI for k in keys):
        # Falta de informação -> Moderado/Sério
        return MODERATE # Potencialmente SERIOUS
    # Se passou por tudo, pode ser Baixo ou Moderado
    # Se houver alguma dúvida (Provavelmente Sim/Não) pode ser Moderado
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d1.values()):
         return MODERATE
    return LOW

def avaliar_dominio_2_robins(respostas_d2):
    keys = ["2.1", "2.2", "2.3", "2.4"]
    # Lógica condicional para 2.2
    required_keys = ["2.1", "2.3", "2.4"]
    if respostas_d2.get("2.1") in YES:
        required_keys.append("2.2")
        
    if check_pending_robins(respostas_d2, required_keys): return PENDING

    if respostas_d2.get("2.1") in YES and respostas_d2.get("2.2") in YES:
        # Seleção pós-intervenção relacionada a intervenção e desfecho -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d2.get("2.3") in NO:
        # Viés de inception -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d2.get("2.1") in YES and respostas_d2.get("2.2") in NO and respostas_d2.get("2.4") in NO:
         # Seleção pós-intervenção, mas não relacionada ao desfecho e sem ajuste -> Moderado?
         return MODERATE
    if any(respostas_d2.get(k) == NI for k in required_keys):
        return MODERATE # Potencialmente SERIOUS
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d2.values()):
         return MODERATE
    return LOW

def avaliar_dominio_3_robins(respostas_d3):
    keys = ["3.1", "3.2", "3.3"]
    if check_pending_robins(respostas_d3, keys): return PENDING

    if respostas_d3.get("3.1") in NO:
        # Classificação incorreta -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d3.get("3.3") in YES:
        # Influenciada pelo desfecho (diferencial) -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d3.get("3.2") in NO:
        # Informação não registrada no início -> Moderado/Sério
        return MODERATE # Potencialmente SERIOUS
    if any(respostas_d3.get(k) == NI for k in keys):
        return MODERATE # Potencialmente SERIOUS
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d3.values()):
         return MODERATE
    return LOW

def avaliar_dominio_4_robins(respostas_d4):
    # Precisa primeiro determinar o efeito de interesse
    effect_interest = respostas_d4.get("4.0_effect", "Não selecionado")
    if effect_interest == "Não selecionado": return PENDING

    if effect_interest == "Efeito da Designação":
        keys = ["4.1_assignment", "4.2_assignment"]
        required_keys = ["4.1_assignment"]
        if respostas_d4.get("4.1_assignment") in YES:
             required_keys.append("4.2_assignment")
        if check_pending_robins(respostas_d4, required_keys): return PENDING
        
        if respostas_d4.get("4.1_assignment") in YES and respostas_d4.get("4.2_assignment") in YES:
            return SERIOUS # Potencialmente CRITICAL
        if any(respostas_d4.get(k) == NI for k in required_keys):
             return MODERATE # Potencialmente SERIOUS
        if any(respostas_d4.get(k) in ["Provavelmente sim", "Provavelmente não"] for k in required_keys):
             return MODERATE
        return LOW
            
    elif effect_interest == "Efeito da Aderência":
        keys = ["4.1_adherence", "4.2_adherence", "4.3_adherence", "4.4_adherence"]
        if check_pending_robins(respostas_d4, keys): return PENDING
        
        if respostas_d4.get("4.4_adherence") in NO:
             return SERIOUS # Análise inadequada
        if respostas_d4.get("4.1_adherence") in NO or \
           respostas_d4.get("4.2_adherence") in YES or \
           respostas_d4.get("4.3_adherence") in YES:
             # Problemas com cointervenções, implementação ou aderência
             return SERIOUS # Potencialmente CRITICAL se análise não ajusta
        if any(respostas_d4.get(k) == NI for k in keys):
             return MODERATE # Potencialmente SERIOUS
        if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d4.values()):
             return MODERATE
        return LOW
    else:
        return PENDING # Efeito de interesse não selecionado

def avaliar_dominio_5_robins(respostas_d5):
    keys = ["5.1", "5.2", "5.3", "5.4"]
    required_keys = ["5.1", "5.2", "5.3"]
    if respostas_d5.get("5.3") in NO:
        required_keys.append("5.4")
    if check_pending_robins(respostas_d5, required_keys): return PENDING

    if respostas_d5.get("5.3") in NO and respostas_d5.get("5.4") in YES:
        # Dados faltantes dependentes do valor verdadeiro -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d5.get("5.1") in NO or respostas_d5.get("5.2") in NO:
        # Proporção não pequena -> Moderado/Sério
        # A distinção depende da proporção e do impacto (não capturado aqui)
        return MODERATE # Potencialmente SERIOUS
    if any(respostas_d5.get(k) == NI for k in required_keys):
        return MODERATE # Potencialmente SERIOUS
    # Se 5.3 é Sim (evidência de não viés), tende a Baixo
    if respostas_d5.get("5.3") in YES:
         return LOW
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d5.values()):
         return MODERATE
    # Se chegou aqui, 5.1/5.2 são Sim, 5.3 é Não/NI, 5.4 é Não/NI
    return MODERATE

def avaliar_dominio_6_robins(respostas_d6):
    keys = ["6.1", "6.2", "6.3", "6.4"]
    required_keys = ["6.1", "6.2", "6.3"]
    if respostas_d6.get("6.3") in YES:
        required_keys.append("6.4")
    if check_pending_robins(respostas_d6, required_keys): return PENDING

    if respostas_d6.get("6.1") in YES or respostas_d6.get("6.2") in YES:
        # Método inadequado ou diferencial -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if respostas_d6.get("6.3") in YES and respostas_d6.get("6.4") in YES:
        # Avaliador ciente e influenciado -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if any(respostas_d6.get(k) == NI for k in required_keys):
        return MODERATE # Potencialmente SERIOUS
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d6.values()):
         return MODERATE
    return LOW

def avaliar_dominio_7_robins(respostas_d7):
    keys = ["7.1", "7.2", "7.3"]
    if check_pending_robins(respostas_d7, keys): return PENDING

    if any(respostas_d7.get(k) in YES for k in keys):
        # Seleção baseada em resultados -> Sério/Crítico
        return SERIOUS # Potencialmente CRITICAL
    if any(respostas_d7.get(k) == NI for k in keys):
        # Falta de informação (ex: protocolo) -> Moderado/Sério
        return MODERATE # Potencialmente SERIOUS
    if any(r in ["Provavelmente sim", "Provavelmente não"] for r in respostas_d7.values()):
         return MODERATE
    return LOW

def avaliar_robins_i_geral(julgamentos_dominios):
    if not julgamentos_dominios or any(j == PENDING for j in julgamentos_dominios.values()):
        return PENDING
    
    judgements_list = list(julgamentos_dominios.values())
    
    if any(j == CRITICAL for j in judgements_list):
        return CRITICAL
    
    serious_count = sum(1 for j in judgements_list if j == SERIOUS)
    moderate_count = sum(1 for j in judgements_list if j == MODERATE)
    no_info_count = sum(1 for j in judgements_list if j == NO_INFO)

    # Regra de escalonamento (exemplo, ajustar conforme orientação oficial)
    if serious_count >= 1: # 1 ou mais sérios -> Sério (pode escalar para Crítico se múltiplos)
        # if serious_count >= 2: return CRITICAL # Exemplo de escalonamento
        return SERIOUS
        
    if moderate_count >= 1: # 1 ou mais moderados -> Moderado (pode escalar para Sério se múltiplos)
        # if moderate_count >= 3: return SERIOUS # Exemplo de escalonamento
        return MODERATE
        
    if no_info_count >= 1:
        # A orientação oficial pode sugerir um julgamento específico (ex: Moderado ou Sério)
        return NO_INFO # Ou MODERATE/SERIOUS

    # Se chegou aqui, todos são LOW
    if all(j == LOW for j in judgements_list):
        return LOW
        
    return NO_INFO # Fallback se algo inesperado ocorrer

def gerar_justificativa_sugerida_robins_i(domain_key, respostas):
    # Reutiliza a função anterior, ajustando nomes se necessário
    domain_info = ROBINS_I_QUESTIONS.get(domain_key)
    if not domain_info: return ""
    
    sugestao = f"Avaliação do {domain_info[\"name\"]}:\n"
    if respostas:
        for q_key, answer in respostas.items():
            # Ignora a pergunta 4.0 sobre efeito de interesse na justificativa
            if q_key == "4.0_effect": continue 
            
            if answer != "Não selecionado":
                question_text = domain_info[\"questions\"]
                question_text_clean = question_text.get(q_key, q_key)
                # Tenta remover prefixo numérico e sufixo de tipo de efeito
                q_key_base = q_key.split(\"")[-1] if \"_\" in q_key else q_key
                parts = question_text_clean.split(\".\")
                if len(parts) > 1 and parts[0].isdigit():
                     # Remove o número inicial e o texto condicional (ex: "(Se Sim...)")
                     text_part = \".\".join(parts[1:]).strip()
                     # Remove texto condicional inicial
                     if text_part.startswith("("):
                         closing_paren = text_part.find(")")
                         if closing_paren != -1:
                             text_part = text_part[closing_paren+1:].strip()
                     # Remove sufixo de tipo de efeito
                     if text_part.endswith("(Efeito da Designação)") or text_part.endswith("(Efeito da Aderência)"):
                          text_part = text_part[:text_part.rfind("(")].strip()
                          
                     question_text_clean = text_part
                     
                if question_text_clean:
                    sugestao += f"- {question_text_clean}: {answer}\n"
    else:
        sugestao += "Nenhuma resposta fornecida ainda.\n"
    return sugestao

def run_robins_i_assessment(responses):
    julgamentos = {}
    avaliadores = {
        "D1": avaliar_dominio_1_robins,
        "D2": avaliar_dominio_2_robins,
        "D3": avaliar_dominio_3_robins,
        "D4": avaliar_dominio_4_robins,
        "D5": avaliar_dominio_5_robins,
        "D6": avaliar_dominio_6_robins,
        "D7": avaliar_dominio_7_robins,
    }
    
    all_domains_answered = True
    for d_key in ROBINS_I_QUESTIONS.keys():
        domain_responses = responses.get(d_key, {})
        julgamentos[d_key] = avaliadores[d_key](domain_responses)
        if julgamentos[d_key] == PENDING:
            all_domains_answered = False
            
    if all_domains_answered:
        julgamentos["Geral"] = avaliar_robins_i_geral({k: v for k, v in julgamentos.items() if k != "Geral"})
    else:
        julgamentos["Geral"] = PENDING
        
    return julgamentos

