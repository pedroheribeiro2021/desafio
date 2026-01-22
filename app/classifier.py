import re
import unicodedata
from transformers import pipeline

# =========================
# MODELO LOCAL 100% GRATUITO
# =========================
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# =========================
# NORMALIZAÇÃO OBRIGATÓRIA
# =========================
def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =========================
# REGRAS DE NEGÓCIO
# =========================
IMPRODUTIVE_KEYWORDS = [
    "feliz natal",
    "boas festas",
    "ano novo",
    "agradeco",
    "agradecemos",
    "parabens",
    "mensagem de natal",
    "abraços",
    "cordialmente"
]

PRODUCTIVE_KEYWORDS = [
    "suporte",
    "erro",
    "problema",
    "falha",
    "status",
    "solicito",
    "solicitacao",
    "chamado",
    "incidente"
]

# =========================
# CLASSIFICAÇÃO
# =========================
def classify_email(text: str) -> str:
    text = normalize_text(text)

    # Regra determinística primeiro (NUNCA IA antes disso)
    if any(word in text for word in IMPRODUTIVE_KEYWORDS):
        return "Improdutivo"

    if any(word in text for word in PRODUCTIVE_KEYWORDS):
        return "Produtivo"

    # Fallback com IA
    labels = [
        "Email que exige ação ou resposta da equipe",
        "Email informativo, promocional ou cordial sem necessidade de ação"
    ]

    result = classifier(text, labels)
    label = result["labels"][0]
    score = result["scores"][0]

    if score < 0.65:
        return "Improdutivo"

    if "exige ação" in label.lower():
        return "Produtivo"

    return "Improdutivo"

# =========================
# RESPOSTA AUTOMÁTICA
# =========================
def generate_reply(category: str) -> str:
    if category == "Produtivo":
        return (
            "Olá,\n\n"
            "Recebemos sua solicitação e ela foi encaminhada para análise da nossa equipe. "
            "Em breve retornaremos com uma atualização.\n\n"
            "Atenciosamente,\nEquipe"
        )
    else:
        return (
            "Olá,\n\n"
            "Agradecemos sua mensagem.\n\n"
            "Atenciosamente,\nEquipe"
        )

# =========================
# RESUMO SIMPLES (SEM OPENAI)
# =========================
def summarize_email(text: str) -> str:
    text = normalize_text(text)
    sentences = re.split(r"[.!?]", text)
    return sentences[0][:120] if sentences else "Resumo não disponível."
