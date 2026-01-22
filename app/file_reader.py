import re
from pypdf import PdfReader

def normalize_content(text: str) -> str:

    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[^\w\s.,!?;:()@#\-]', '', text)
    
    text = text.lower().strip()
    
    return text

def read_txt(file) -> str:

    try:
        content = file.file.read().decode("utf-8", errors="ignore")
        return normalize_content(content)
    except Exception as e:
        print(f"Erro leitura TXT: {e}")
        return ""

def read_pdf(file) -> str:

    try:
        reader = PdfReader(file.file)
        text = ""
        
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            except Exception:
                continue
        
        return normalize_content(text)
        
    except Exception as e:
        print(f"Erro leitura PDF: {e}")
        return ""