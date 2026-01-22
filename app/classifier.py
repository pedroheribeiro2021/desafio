import re
import unicodedata
from typing import Dict


IMP_PROFESSIONAL_CONTEXT = {
    "informal_greetings": ["oi", "olá", "eae", "fala", "beleza", "tudo bem"],
    "personal_topics": ["vc", "você", "vida pessoal", "namorado", "namorada"],
    "social": ["feliz", "natal", "ano novo", "parabéns", "comemoração", "festas", "boas festas"],
    "marketing": ["promoção", "desconto", "oferta", "clique aqui", "marketing", "divulgação"],
    "irrelevant": ["curiosidade", "divulgar", "compartilhar", "artigo", "interessante", "dica"]
}

PRO_BUSINESS_CONTEXT = {
    "technical_issues": ["erro", "falha", "bug", "não funciona", "problema", "quebra", 
                        "indisponível", "processar", "pagamento", "sistema", "técnico"],
    "requests": ["solicito", "solicitação", "pedido", "requisição", "formalizar", 
                "suporte", "ajuda", "assistência", "chamado", "ticket", "urgente"],
    "status_updates": ["status", "andamento", "atualização", "prazo", "previsão", "resolução"],
    "financial": ["pagamento", "fatura", "boleto", "transação", "saldo", "extrato",
                 "pagamentos", "processar faturas", "gateway", "crédito", "débito"]
}

def analyze_business_context(text: str) -> Dict[str, int]:

    text_lower = text.lower()
    
    personal_score = 0
    for category, words in IMP_PROFESSIONAL_CONTEXT.items():
        for word in words:
            if word in text_lower:
                personal_score += 2 if category == "personal_topics" else 1
    
    business_score = 0
    for category, words in PRO_BUSINESS_CONTEXT.items():
        for word in words:
            if word in text_lower:
                business_score += 4 if category in ["technical_issues", "requests"] else 2
    
    structure_score = 0
    sentences = re.split(r'[.!?]+', text)
    
    if len(sentences) > 3:
        structure_score += 2
    
    if any(word in text_lower for word in ["problema", "erro", "falha"]):
        if any(word in text_lower for word in ["solução", "resolver", "consertar"]):
            structure_score += 2
    
    if re.search(r'\d+', text):
        structure_score += 1
    
    return {
        "personal_score": personal_score,
        "business_score": business_score,
        "structure_score": structure_score,
        "total_business": business_score + structure_score,
        "total_personal": personal_score
    }


def classify_email(text: str) -> str:

    if not text or len(text.strip()) < 10:
        return "Improdutivo"
    
    try:
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = text.lower().strip()
    except Exception:
        text = text.lower().strip()
    
    inappropriate_patterns = [
        r"(?:^|\s)(vc\s+[^\?]+\?)",
        r"(e\s+voc[êe]\??$)",
        r"(vida\s+pessoal)",
        r"(conhecer\s+pessoalmente)",
        
        r"(promo[cç][aã]o|desconto|oferta).*(clique|link|site)",
        r"(marketing|publicidade|divulga[cç][aã]o)",
        
        r"^(oi|ol[aá]|eae|fala).{0,30}$",
    ]
    
    for pattern in inappropriate_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"[DEBUG] Padrão inapropriado encontrado: {pattern}")
            return "Improdutivo"
    
    try:
        context = analyze_business_context(text)
        print(f"[DEBUG] Análise contexto: {context}")
        
        if context["total_personal"] > 3:
            return "Improdutivo"
        
        tech_keywords = ["urgente", "problema", "erro", "falha", "não funciona", "suporte"]
        if any(keyword in text for keyword in tech_keywords):
            if context["business_score"] >= 2: 
                return "Produtivo"
        
        if context["business_score"] >= 4:
            return "Produtivo"
        
        if context["total_business"] >= 6:
            return "Produtivo"
        
        return "Improdutivo"
        
    except Exception as e:
        print(f"[ERROR] Erro na classificação: {e}")
        return "Improdutivo"


def generate_reply(category: str, original_text: str = "") -> str:

    if not category:
        category = "Improdutivo"
    
    original_lower = original_text.lower() if original_text else ""
    inappropriate = any(
        term in original_lower 
        for term in ["gay", "lésbica", "trans", "vida pessoal", "vc?", "você?"]
    )
    
    if inappropriate:
        return (
            "Olá,\n\n"
            "Esta caixa de email é destinada exclusivamente a assuntos profissionais "
            "relacionados a nossos serviços financeiros.\n\n"
            "Para questões pessoais ou não relacionadas aos nossos serviços, "
            "sugerimos utilizar os canais apropriados.\n\n"
            "Atenciosamente,\nEquipe de Suporte"
        )
    
    if category == "Produtivo":
        return (
            "Olá,\n\n"
            "Recebemos sua solicitação relacionada aos nossos serviços financeiros. "
            "Seu caso foi registrado sob o protocolo #[AUTO-GERADO] e será analisado "
            "pela nossa equipe especializada.\n\n"
            "Você receberá uma atualização em até 24 horas úteis.\n\n"
            "Atenciosamente,\nEquipe de Suporte Financeiro"
        )
    else:
        return (
            "Olá,\n\n"
            "Agradecemos seu contato. Esta mensagem foi identificada como informativa.\n\n"
            "Caso tenha uma solicitação específica relacionada a nossos serviços "
            "financeiros, por favor reformule sua mensagem incluindo detalhes como:\n"
            "- Número de protocolo (se aplicável)\n"
            "- Descrição do assunto financeiro\n"
            "- Qual ação necessária\n\n"
            "Atenciosamente,\nEquipe de Suporte"
        )


def summarize_email(text: str) -> str:

    try:
        sentences = re.split(r'[.!?]+', text)
        
        greeting_patterns = [
            r'^(olá|oi|bom dia|boa tarde|boa noite|prezados|caros)',
            r'^(email|mensagem).*(segue|encaminho)',
            r'^assunto:',
            r'^de:',
            r'^para:'
        ]
        
        content_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 15:
                continue
            if any(re.match(pattern, sentence.lower()) for pattern in greeting_patterns):
                continue
            content_sentences.append(sentence)
        
        if not content_sentences:
            return text[:120] + ("..." if len(text) > 120 else "")
        
        for sentence in content_sentences:
            if len(sentence.split()) >= 5:  
                return sentence[:150] + ("..." if len(sentence) > 150 else "")
        
        return content_sentences[0][:120] + "..."
    except Exception:
        return text[:100] + "..."



    
