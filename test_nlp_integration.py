from nlp_processor import preprocess_email_text, get_email_keywords
from classifier import classify_email

def test_nlp_pipeline():
    print("🧪 TESTE RÁPIDO DA INTEGRAÇÃO NLP")
    print("=" * 60)
    
    email_produtivo = "Problema urgente no sistema de pagamentos, erro 500"
    
    print(f"\n📧 EMAIL DE TESTE: '{email_produtivo}'")
    print("-" * 40)
    
    processed = preprocess_email_text(email_produtivo)
    print(f"\n1. Texto processado por NLP:")
    print(f"   '{processed}'")
    
    keywords = get_email_keywords(email_produtivo, top_n=5)
    print(f"\n2. Palavras-chave extraídas:")
    for word, freq in keywords:
        print(f"   {word}: {freq}")
    
    categoria = classify_email(email_produtivo)
    print(f"\n3. Classificação final: {categoria}")
    print(f"\n✅ RESULTADO: {categoria} (esperado: Produtivo)")
    
    print("\n" + "=" * 60)
    print("🧪 TESTES RÁPIDOS ADICIONAIS")
    print("=" * 60)
    
    testes = [
        ("Problema urgente no sistema de pagamentos, erro crítico", "Produtivo"),
        ("Feliz Natal a todos os colegas!", "Improdutivo"),
        ("Solicito alteração na fatura #1234", "Produtivo"),
        ("Oi, tudo bem? Como vai você?", "Improdutivo"),
        ("URGENTE: Falha crítica no processamento", "Produtivo"),
    ]
    
    for texto, esperado in testes:
        resultado = classify_email(texto)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} '{texto[:40]}...' -> {resultado}")

if __name__ == "__main__":
    test_nlp_pipeline()