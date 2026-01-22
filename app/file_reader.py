from pypdf import PdfReader
import re

def read_txt(file) -> str:

    try:
        content = file.file.read()
        
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('latin-1', errors='ignore')
        
        text = re.sub(r'\r\n', '\n', text)  
        text = re.sub(r'\n{3,}', '\n\n', text)  
        
        return text.strip()
        
    except Exception as e:
        print(f"[FILE READER ERROR TXT] {e}")
        return ""

def read_pdf(file) -> str:
    """
    Lê arquivo PDF e extrai texto preservando conteúdo.
    """
    try:
        reader = PdfReader(file.file)
        text = ""
        
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception:
                continue
        
        text = re.sub(r'\s+', ' ', text)  
        text = re.sub(r'\n\s*\n', '\n\n', text)  
        
        return text.strip()
        
    except Exception as e:
        print(f"[FILE READER ERROR PDF] {e}")
        return ""

def normalize_content(text: str) -> str:

    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[^\w\s.,!?;:()@#\-\n]', '', text)
    
    return text.strip()