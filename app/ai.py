from transformers import pipeline

# Modelo 100% gratuito, roda local
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

PROMO_KEYWORDS = [
    "promoção", "oferta", "desconto", "compre",
    "clique", "marketing", "publicidade"
]

def classify_email(text: str) -> str:
    # Regra de negócio primeiro (híbrido)
    lower_text = text.lower()
    if any(word in lower_text for word in PROMO_KEYWORDS):
        return "Improdutivo"

    labels = [
        "Email que exige ação ou resposta da equipe",
        "Email informativo, promocional ou cordial sem necessidade de ação"
    ]

    prompt = f"""
    Considere o seguinte email recebido por uma empresa do setor financeiro.

    Classifique como:
    - Produtivo: exige resposta, ação ou acompanhamento.
    - Improdutivo: apenas informativo, promocional ou cordial.

    Email:
    {text}
    """

    result = classifier(prompt, labels)

    label = result["labels"][0]
    score = result["scores"][0]

    # Threshold de segurança
    if score < 0.65:
        return "Improdutivo"

    if "exige ação" in label:
        return "Produtivo"

    return "Improdutivo"


def generate_reply(category: str) -> str:
    if category == "Produtivo":
        return (
            "Olá,\n\n"
            "Recebemos sua mensagem e ela foi encaminhada para análise da nossa equipe. "
            "Retornaremos o mais breve possível.\n\n"
            "Atenciosamente,\nEquipe"
        )
    else:
        return (
            "Olá,\n\n"
            "Agradecemos sua mensagem.\n\n"
            "Atenciosamente,\nEquipe"
        )
