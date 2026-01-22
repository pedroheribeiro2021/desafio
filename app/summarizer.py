import re
from collections import Counter

def summarize_email(text: str) -> str:
    if not text.strip():
        return "Não foi possível identificar o tema."

    sentences = re.split(r'[.!?]\s+', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 5]

    if not sentences:
        return "Email curto ou sem conteúdo relevante."

    words = re.findall(r'\b[a-záàâãéêíóôõúç]+\b', text.lower())
    stopwords = {
        "de","a","o","que","e","do","da","em","um","para","é","com",
        "não","uma","os","no","se","na","por","mais","as","dos"
    }

    words = [w for w in words if w not in stopwords]
    freq = Counter(words)

    def score(sentence):
        return sum(freq.get(w.lower(), 0) for w in sentence.split())

    best_sentence = max(sentences, key=score)
    return best_sentence
