from classifier import classify_email

print("🎯 TESTE RÁPIDO DO CLASSIFICADOR")
print("=" * 60)

testes_criticos = [
    ("Problema urgente no sistema de pagamentos, erro 500", "Produtivo", "Problema técnico"),
    ("Feliz Natal e próspero Ano Novo a todos!", "Improdutivo", "Mensagem social"),
    ("Solicito alteração na fatura #1234 com urgência", "Produtivo", "Solicitação formal"),
    ("Oi, tudo bem? Como vai você?", "Improdutivo", "Mensagem pessoal"),
    ("Bom dia, preciso do status do meu pedido #5678", "Produtivo", "Consulta de status"),
    ("Prezados, compartilho artigo interessante", "Improdutivo", "Compartilhamento"),
    ("URGENTE: Sistema fora do ar, clientes afetados", "Produtivo", "Incidente crítico"),
    ("Agradeço a todos pelo trabalho", "Improdutivo", "Agradecimento"),
]

print("\n📊 RESULTADOS:")
print("-" * 60)

acertos = 0
for texto, esperado, descricao in testes_criticos:
    resultado = classify_email(texto)
    correto = resultado == esperado
    if correto:
        acertos += 1
        print(f"✅ {descricao}")
    else:
        print(f"❌ {descricao}")
    print(f"   Texto: '{texto[:50]}...'")
    print(f"   Esperado: {esperado}, Obtido: {resultado}")
    print()

print(f"\n📈 ACURÁCIA: {acertos}/{len(testes_criticos)} ({acertos/len(testes_criticos)*100:.0f}%)")
print("=" * 60)

print("\n📧 TESTE COM EMAIL COMPLETO DO DESAFIO:")
print("-" * 60)

email_completo = """
Assunto: Solicitação de suporte técnico - Sistema não processa pagamentos
De: maria.silva@empresax.com.br
Para: suporte@financeiro.com

Bom dia,

Estou com um problema urgente no sistema de pagamentos. Desde ontem às 16h, todas as tentativas de processar faturas estão retornando erro 'Conexão com gateway indisponível'.

Já tentei:
1. Reiniciar a aplicação
2. Verificar as credenciais da API
3. Testar em outro navegador

O problema persiste. Conseguem priorizar essa análise? Temos 50 pagamentos pendentes e clientes aguardando.

Por favor, me confirmem um prazo para resolução.

Atenciosamente,
Maria Silva
Gerente Financeira
"""

resultado_final = classify_email(email_completo)
print(f"Email produtivo (sistema pagamentos):")
print(f"Resultado: {resultado_final}")
print(f"✅ DEVERIA SER: Produtivo")