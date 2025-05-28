# utils/export_utils.py
import pandas as pd
from io import BytesIO
from weasyprint import HTML

# --- Funções de Exportação Base ---

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

def exportar_para_pdf(html_content):
    """Converte conteúdo HTML para PDF usando WeasyPrint."""
    if not html_content:
        return None
    try:
        pdf_buffer = BytesIO()
        # Assume que o CSS está incluído no próprio HTML ou é referenciado nele
        HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

