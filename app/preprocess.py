import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\W+", " ", text)
    words = text.split()
    filtered = [w for w in words if w not in stopwords.words("portuguese")]
    return " ".join(filtered)
