import re

def normalize_email_text(text: str) -> str:
    text = text.lower()

    # Remove cabeçalhos comuns
    text = re.sub(r"(assunto|de|para):.*", "", text)

    # Remove emails
    text = re.sub(r"\S+@\S+", "", text)

    # Remove excesso de espaços
    text = re.sub(r"\s+", " ", text)

    return text.strip()
