# utils/export.py
import pandas as pd
from io import BytesIO
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

# --- Funções de Exportação (Genéricas ou Adaptadas) ---

def exportar_para_csv(df: pd.DataFrame):
    """Converte um DataFrame pandas para bytes CSV prontos para download."""
    if df is None or df.empty:
        return None
    try:
        csv_buffer = BytesIO()
        # Usar utf-8-sig para melhor compatibilidade com Excel
        df.to_csv(csv_buffer, index=False, encoding=\'utf-8-sig\')
        csv_buffer.seek(0)
        return csv_buffer.getvalue()
    except Exception as e:
        print(f"Erro ao gerar CSV: {e}") # Log do erro
        return None

def gerar_html_relatorio_robins_i(study_info, df_results):
    """Renderiza o template HTML específico para ROBINS-I com os dados."""
    try:
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"assets\"))
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(\"report_template_robins_i.html\")

        # Prepara o contexto, incluindo informações PICO
        context = {
            \"study_id\": study_info.get(\"id\", \"Não informado\"),
            \"outcome\": study_info.get(\"outcome\", \"Não informado\"),
            \"pico_p\": study_info.get(\"pico_p\", \"Não informado\"),
            \"pico_i\": study_info.get(\"pico_i\", \"Não informado\"),
            \"pico_c\": study_info.get(\"pico_c\", \"Não informado\"),
            \"pico_o\": study_info.get(\"pico_o\", \"Não informado\"),
            \"effect_interest\": study_info.get(\"effect_interest\", \"Não informado\"),
            \"results\": df_results.to_dict(orient=\"records\")
        }

        html_content = template.render(context)
        return html_content
    except Exception as e:
        print(f"Erro ao gerar HTML do relatório ROBINS-I: {e}")
        return None

def exportar_para_pdf(html_content):
    """Converte conteúdo HTML para PDF usando WeasyPrint (genérico)."""
    if not html_content:
        return None
    try:
        pdf_buffer = BytesIO()
        # O CSS é incluído no template HTML
        HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

