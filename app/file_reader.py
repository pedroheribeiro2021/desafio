from pypdf import PdfReader

def read_txt(file) -> str:
    try:
        return file.file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""

def read_pdf(file) -> str:
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

        return text.strip()

    except Exception:
        return ""
