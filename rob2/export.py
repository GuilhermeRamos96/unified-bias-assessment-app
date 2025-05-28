# utils/export.py
import pandas as pd
from io import BytesIO
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

def exportar_para_csv(df: pd.DataFrame):
    """Converte um DataFrame pandas para bytes CSV prontos para download."""
    if df is None or df.empty:
        return None
    try:
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding=\'utf-8-sig\')
        csv_buffer.seek(0)
        return csv_buffer.getvalue()
    except Exception as e:
        print(f"Erro ao gerar CSV: {e}")
        return None

def gerar_html_relatorio(study_info, df_results):
    """Renderiza o template HTML com os dados."""
    try:
        # Configura o ambiente Jinja2 para carregar o template da pasta assets
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), \'..\', \'assets\'))
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(\'report_template.html\')

        # Prepara os dados para o template
        context = {
            \'study_id\': study_info.get(\'id\', \'Não informado\'),
            \'outcome\': study_info.get(\'outcome\', \'Não informado\'),
            \'results\': df_results.to_dict(orient=\'records\') # Converte DataFrame para lista de dicionários
            # Adicionar caminho do gráfico se for gerado como imagem estática
            # \'graph_path\': graph_path 
        }

        # Renderiza o HTML
        html_content = template.render(context)
        return html_content
    except Exception as e:
        print(f"Erro ao gerar HTML do relatório: {e}")
        return None

def exportar_para_pdf(html_content):
    """Converte conteúdo HTML para PDF usando WeasyPrint."""
    if not html_content:
        return None
    try:
        pdf_buffer = BytesIO()
        # CSS pode ser incluído diretamente no HTML ou carregado separadamente
        # css = CSS(string=\'@page { size: A4; margin: 1.5cm; }\') # Exemplo de CSS
        HTML(string=html_content).write_pdf(pdf_buffer) # , stylesheets=[css]
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

