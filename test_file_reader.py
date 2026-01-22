from file_reader import read_txt
import io

test_text = """INCIDENTE CRÍTICO - Sistema de Cobrança Fora do Ar

Bom dia Equipe,

O sistema de cobrança está completamente inoperante desde às 08:30 desta manhã. 

Tentativas de acesso resultam em erro HTTP 500. Já verifiquei:
- Acesso à rede corporativa ✓
- Credenciais válidas ✓
- Aplicativo atualizado ✓

Impacto: 120 clientes não conseguem realizar pagamentos neste momento.

Solicito:
1. Prioridade máxima neste incidente
2. Atualização a cada 30 minutos
3. ETA para normalização

Precisamos de retorno IMEDIATO."""

class FakeFile:
    def __init__(self, content):
        self.file = io.BytesIO(content.encode('utf-8'))
        self.filename = "teste.txt"

print("🧪 TESTE LEITURA TXT vs TEXTO DIRETO")
print("=" * 60)

fake_file = FakeFile(test_text)
texto_do_arquivo = read_txt(fake_file)

print(f"Texto original (primeiros 100 chars):")
print(f"'{test_text[:100]}...'")
print(f"\nTexto lido do arquivo (primeiros 100 chars):")
print(f"'{texto_do_arquivo[:100]}...'")
print(f"\nSão IGUAIS? {test_text[:100] == texto_do_arquivo[:100]}")

from classifier import classify_email

print(f"\n🎯 TESTE CLASSIFICAÇÃO:")
print(f"Texto direto: {classify_email(test_text)}")
print(f"Texto do arquivo: {classify_email(texto_do_arquivo)}")
print(f"Resultados IGUAIS? {classify_email(test_text) == classify_email(texto_do_arquivo)}")