import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def display_pdf(uploaded_file):
    """Exibe um arquivo PDF carregado na interface do Streamlit, uma página por vez."""
    if uploaded_file is not None:
        try:
            # Lê os bytes do arquivo carregado
            pdf_bytes = uploaded_file.getvalue()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            total_pages = len(doc)
            if total_pages > 0:
                st.write(f"Visualizador de PDF ({total_pages} páginas)")
                
                # Selecionador de página
                page_num = st.number_input("Ir para página", min_value=1, max_value=total_pages, value=1, step=1)
                
                # Renderiza a página selecionada como imagem
                page = doc.load_page(page_num - 1)  # page_num é 1-based, índice é 0-based
                pix = page.get_pixmap(dpi=150) # Aumenta DPI para melhor qualidade
                
                # Converte para formato de imagem que o Streamlit entende (PIL)
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                
                st.image(img, caption=f"Página {page_num}/{total_pages}", use_column_width=True)
            else:
                st.warning("O arquivo PDF parece estar vazio ou não pôde ser lido.")
            doc.close()
        except Exception as e:
            st.error(f"Erro ao processar o PDF: {e}")
            st.warning("Certifique-se de que o arquivo é um PDF válido e não está corrompido.")
    else:
        st.info("Carregue um arquivo PDF na barra lateral para visualizá-lo aqui.")

