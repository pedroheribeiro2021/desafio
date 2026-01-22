from transformers import pipeline

# 🔹 Classificador zero-shot (local)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# 🔹 Summarizador local (leve e gratuito)
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

PROMO_KEYWORDS = [
    "promoção", "oferta", "desconto", "compre",
    "clique", "marketing", "publicidade"
]


def classify_email(text: str) -> str:
    lower_text = text.lower()

    # 🚦 Regra de negócio explícita (anti-spam)
    if any(word in lower_text for word in PROMO_KEYWORDS):
        return "Improdutivo"

    labels = [
        "Email que exige ação ou resposta da equipe",
        "Email informativo ou cordial sem necessidade de ação"
    ]

    result = classifier(text, labels)

    label = result["labels"][0]
    score = result["scores"][0]

    # Threshold de segurança
    if score < 0.65:
        return "Improdutivo"

    if "exige ação" in label:
        return "Produtivo"

    return "Improdutivo"


def summarize_email(text: str) -> str:
    # Proteção para textos muito longos
    text = text[:2000]

    result = summarizer(
        text,
        max_length=30,
        min_length=10,
        do_sample=False
    )

    return result[0]["summary_text"]


def generate_reply(category: str) -> str:
    if category == "Produtivo":
        return (
            "Olá,\n\n"
            "Recebemos sua solicitação e ela foi encaminhada para análise da nossa equipe. "
            "Em breve retornaremos com mais informações.\n\n"
            "Atenciosamente,\nEquipe"
        )
    else:
        return (
            "Olá,\n\n"
            "Agradecemos sua mensagem.\n\n"
            "Atenciosamente,\nEquipe"
        )
