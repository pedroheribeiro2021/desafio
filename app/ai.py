import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_email(text: str) -> str:
    prompt = f"""
Classifique o email abaixo como Produtivo ou Improdutivo.

Email:
{text}

Responda apenas com uma palavra.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_reply(text: str, category: str) -> str:
    prompt = f"""
Gere uma resposta corporativa educada para o email abaixo.
Categoria: {category}

Email:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
