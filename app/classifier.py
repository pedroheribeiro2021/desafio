import re
import unicodedata
from typing import Dict

from nlp_processor import preprocess_email_text, get_email_keywords


IMP_PROFESSIONAL_CONTEXT = {
    "informal_greetings": ["oi", "olá", "eae", "fala", "beleza", "tudo bem", "td bem"],
    "personal_topics": ["vc", "voc", "vida pessoal", "gay", "lesb", "trans", "namorad"],
    "social": ["feliz", "natal", "ano nov", "paraben", "comemor", "fest", "boas fest"],
    "marketing": ["promoc", "descont", "ofert", "clique aqui", "market", "divulg"],
    "irrelevant": ["curiosidad", "divulg", "compartilh", "artig", "interess", "dic"]
}

PRO_BUSINESS_CONTEXT = {
    "technical_issues": ["err", "falah", "bug", "nao funcion", "problem", "quebr", 
                        "indispon", "process", "pagament", "sistem", "tecnic", 
                        "falh", "inoper", "crash", "conex", "gateway"],
    "requests": ["solicit", "solicitac", "pedid", "requisic", "formaliz", 
                "suport", "ajud", "assist", "chamad", "ticket", "urgent",
                "prioridad", "imedi", "rapid", "asap"],
    "status_updates": ["status", "andament", "atualizac", "praz", "previs", "resoluc",
                      "atualiz", "andament", "praz", "previs", "resoluc"],
    "financial": ["pagament", "fatur", "bolet", "transac", "sald", "extrat",
                 "pagament", "process fatur", "gateway", "credit", "debit",
                 "financ", "cobranc", "receb", "transfer"]
}

def analyze_business_context(text: str) -> Dict[str, int]:

    processed_text = preprocess_email_text(text)
    print(f"[NLP Classifier] Texto processado: {processed_text[:150]}...")
    
    keywords = get_email_keywords(text, top_n=15)
    print(f"[NLP Classifier] Top keywords: {keywords}")
    
    import re
    
    sentences = re.split(r'[.!?]+', text)
    has_numbers = bool(re.search(r'\d+', text))
    has_urgency = any(word in text.lower() for word in ['urgente', 'prioridade', 'imediato', 'asap'])
    has_greeting = any(word in text.lower() for word in ['prezado', 'caro', 'olá', 'bom dia'])
    has_signature = any(word in text.lower() for word in ['atenciosamente', 'cordialmente', 'att'])
    
    personal_score = 0
    for category, words in IMP_PROFESSIONAL_CONTEXT.items():
        for word in words:
            if word in processed_text:
                personal_score += 3 if category == "personal_topics" else 2
    
    business_score = 0
    for category, words in PRO_BUSINESS_CONTEXT.items():
        for word in words:
            if word in processed_text:
                business_score += 5 if category in ["technical_issues", "requests"] else 3
    
    structure_bonus = 0
    
    if len(sentences) > 4:
        structure_bonus += 2
    
    if has_numbers:
        structure_bonus += 2
    
    if has_urgency:
        structure_bonus += 3
    
    if has_greeting and has_signature:
        structure_bonus += 2
    
    print(f"[NLP Classifier] Scores - Personal: {personal_score}, Business: {business_score}, Structure: {structure_bonus}")
    
    return {
        "personal_score": personal_score,
        "business_score": business_score,
        "structure_score": structure_bonus,
        "total_business": business_score + structure_bonus,
        "total_personal": personal_score,
        "has_urgency": has_urgency,
        "total_sentences": len(sentences)
    }

def classify_email(text: str) -> str:

    if not text or len(text.strip()) < 10:
        print("[NLP Classifier] Texto muito curto -> Improdutivo")
        return "Improdutivo"
    
    print(f"\n{'='*60}")
    print("[NLP Classifier] INICIANDO CLASSIFICAÇÃO COM NLP")
    print(f"{'='*60}")
    
    try:
        context = analyze_business_context(text)
        
        print(f"[NLP Classifier] Resultados análise: Personal={context['total_personal']}, Business={context['total_business']}")
        
        if context['total_personal'] > 4:
            print("[NLP Classifier] Muitos indicadores pessoais -> Improdutivo")
            return "Improdutivo"
        
        tech_keywords = ["urgent", "prioridad", "imedi", "problem", "err", "falah", "suport"]
        processed_text = preprocess_email_text(text)
        
        has_tech_keyword = any(keyword in processed_text for keyword in tech_keywords)
        if has_tech_keyword and context['business_score'] >= 3:
            print(f"[NLP Classifier] Keywords técnicos + business score {context['business_score']} -> Produtivo")
            return "Produtivo"
        
        if context['business_score'] >= 6:
            print(f"[NLP Classifier] Business score alto ({context['business_score']}) -> Produtivo")
            return "Produtivo"
        
        if context['total_business'] >= 8:
            print(f"[NLP Classifier] Total business alto ({context['total_business']}) -> Produtivo")
            return "Produtivo"
        
        if context['features']['has_urgency'] and context['features']['total_sentences'] > 3:
            print("[NLP Classifier] Urgência + email estruturado -> Produtivo")
            return "Produtivo"
        
        print("[NLP Classifier] Fallback conservador -> Improdutivo")
        return "Improdutivo"
        
    except Exception as e:
        print(f"[NLP Classifier ERROR] Erro na classificação: {e}")
        return "Improdutivo"

def generate_reply(category: str, original_text: str = "") -> str:

    if not category:
        category = "Improdutivo"
    
    keywords = []
    try:
        if original_text:
            keywords = get_email_keywords(original_text, top_n=5)
            keywords = [word for word, freq in keywords]
            print(f"[NLP Reply] Keywords para resposta: {keywords}")
    except:
        pass
    
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
        reply = "Olá,\n\n"
        
        if any(word in original_lower for word in ["urgente", "prioridade", "imediato"]):
            reply += "**IDENTIFICAMOS URGÊNCIA NA SUA SOLICITAÇÃO**\n\n"
        
        reply += "Recebemos sua solicitação relacionada aos nossos serviços financeiros. "
        
        if keywords:
            reply += f"Identificamos que o assunto envolve: {', '.join(keywords[:3])}.\n\n"
        
        reply += (
            "Seu caso foi registrado sob o protocolo #[AUTO-GERADO] e será analisado "
            "pela nossa equipe especializada com prioridade.\n\n"
            "Você receberá uma atualização em até 24 horas úteis.\n\n"
            "Atenciosamente,\nEquipe de Suporte Financeiro"
        )
        
        return reply
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
        from nlp_processor import nlp_processor
        
        sentences = nlp_processor.tokenize_sentences(text)
        
        if not sentences:
            return text[:120] + ("..." if len(text) > 120 else "")
        
        cleaned_sentences = []
        greeting_patterns = [
            r'^(olá|oi|bom dia|boa tarde|boa noite|prezados|caros|ilustríssimos)',
            r'^(assunto:|de:|para:|cc:|enc:|reply to:)',
            r'^(segue|encaminho|envio|remeto)'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  
                continue
            
            if any(re.match(pattern, sentence.lower()) for pattern in greeting_patterns):
                continue
            
            cleaned_sentences.append(sentence)
        
        if not cleaned_sentences:
            return sentences[0][:150] + "..." if len(sentences[0]) > 150 else sentences[0]
        
        return cleaned_sentences[0][:150] + ("..." if len(cleaned_sentences[0]) > 150 else "")
        
    except Exception as e:
        print(f"[NLP Summarize Error] {e}")
        return text[:100] + "..."

if __name__ == "__main__":
    print("🧪 TESTANDO CLASSIFICADOR COM NLP")
    
    test_cases = [
        ("Problema urgente no sistema de pagamentos, erro 500", "Produtivo"),
        ("Feliz Natal e próspero Ano Novo a todos!", "Improdutivo"),
        ("Solicito alteração na fatura #1234 com urgência", "Produtivo"),
        ("Oi, tudo bem? Como vai você?", "Improdutivo"),
        ("Bom dia, preciso do status do meu pedido #5678", "Produtivo"),
    ]
    
    for i, (text, expected) in enumerate(test_cases, 1):
        result = classify_email(text)
        status = "✅" if result == expected else "❌"
        print(f"{status} Teste {i}: '{text[:30]}...' -> {result} (esperado: {expected})")
    
    print("\n" + "="*60)
    print("✅ CLASSIFICADOR COM NLP IMPLEMENTADO")
    print("="*60)