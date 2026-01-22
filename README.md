# 📧 Analisador Inteligente de Emails - Desafio Técnico

## 🎯 Sobre o Projeto
Solução web completa para automatizar a leitura e classificação de emails em ambiente corporativo financeiro. O sistema utiliza Processamento de Linguagem Natural (NLP) para classificar emails como **Produtivo** ou **Improdutivo** e gerar respostas automáticas contextualizadas.

## ✨ Funcionalidades Principais
- **📤 Upload flexível**: Texto direto ou arquivos (.txt, .pdf)
- **🤖 Classificação inteligente**: NLP com tokenização, stopwords e stemming em português
- **💬 Respostas automáticas**: Sugestões contextualizadas por categoria
- **🎨 Interface moderna**: Design responsivo com drag & drop
- **🔍 Análise detalhada**: Exibe classificação, resumo e resposta sugerida

## 🛠️ Tecnologias Utilizadas
- **Backend**: Python 3.10 + FastAPI
- **NLP**: Processamento de texto em português com técnicas avançadas
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Hospedagem**: Render.com (Free Tier)
- **Versionamento**: Git + GitHub

## 🚀 Demonstração Online
A aplicação está disponível em: [INSIRA SEU LINK DO RENDER AQUI]

## 📁 Estrutura do Projeto


## 🧠 Como a IA Funciona
### **Pré-processamento NLP:**
1. **Tokenização**: Divisão do texto em palavras/sentenças
2. **Normalização**: Remoção de acentos, conversão para minúsculas
3. **Stopwords**: Remoção de palavras comuns sem valor semântico
4. **Stemming**: Redução de palavras aos seus radicais (ex: "pagamentos" → "pagament")

### **Classificação:**
- **Regras baseadas em keywords**: +50 palavras-chave contextuais
- **Análise estrutural**: Detecção de urgência, formalidade, especificidade
- **Pontuação ponderada**: Combinação de múltiplos fatores

### **Exemplos de Classificação:**
- ✅ **PRODUTIVO**: "Problema urgente no sistema de pagamentos, erro HTTP 500"
- ✅ **IMPRODUTIVO**: "Feliz Natal e próspero Ano Novo a todos!"
- ✅ **PRODUTIVO**: "Solicito alteração na fatura #1234 com urgência"

## 💻 Como Executar Localmente

### Pré-requisitos:
- Python 3.10 ou superior
- Git (opcional)

### Passos:
```bash
# 1. Clone o repositório
git clone https://github.com/[seu-usuario]/email-analyzer.git
cd email-analyzer

# 2. Navegue para a pasta app
cd app

# 3. Crie e ative ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Execute o servidor
uvicorn main:app --reload

# 6. Acesse no navegador
# http://localhost:8000