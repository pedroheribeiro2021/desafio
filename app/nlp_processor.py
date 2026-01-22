import re
import string
import unicodedata
from typing import List, Tuple
from collections import Counter

class NLPProcessor:
    
    def __init__(self):

        self.stop_words_pt = {
            'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para',
            'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais',
            'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem',
            'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos',
            'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso',
            'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter',
            'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você',
            'tinha', 'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às',
            'minha', 'têm', 'numa', 'pelos', 'elas', 'havia', 'seja',
            'qual', 'será', 'nós', 'tenho', 'lhe', 'deles', 'essas',
            'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te', 'vocês',
            'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas',
            'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta',
            'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas',
            'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive',
            'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos',
            'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos',
            'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver',
            'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão',
            'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos',
            'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos',
            'houvessem', 'houver', 'houvermos', 'houverem', 'houverei',
            'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos',
            'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram',
            'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja',
            'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for',
            'formos', 'forem', 'serei', 'será', 'seremos', 'serão',
            'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'têm',
            'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos',
            'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos',
            'tenham', 'tivesse', 'tivéssemos', 'tivessem', 'tiver',
            'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão',
            'teria', 'teríamos', 'teriam'
        }
        
        self.custom_stopwords = {
            'atenciosamente', 'cordialmente', 'sinceramente', 'att',
            'grato', 'obrigado', 'obrigada', 'favor',
            'segue', 'encaminho', 'encaminhando', 'anexo', 'em anexo',
            'prezado', 'prezada', 'caros', 'caras', 'ilmo', 'ilma',
            'senhor', 'senhora', 'sr', 'sra', 'dr', 'dra'
        }
        
        self.all_stopwords = self.stop_words_pt.union(self.custom_stopwords)
    
    
    def normalize_text(self, text: str) -> str:

        if not text:
            return ""
        
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        
        text = text.lower()
        
        text = re.sub(r'\S+@\S+', '', text)  
        text = re.sub(r'http\S+', '', text)  
        text = re.sub(r'(assunto|de|para|cc):.*', '', text, flags=re.IGNORECASE)
        
        text = re.sub(r'[^\w\s\d.,!?;:]', '', text)
        
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize_words(self, text: str) -> List[str]:

        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t.strip()]
    
    def tokenize_sentences(self, text: str) -> List[str]:

        sentences = re.split(r'[.!?]+[\s\n]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [word for word in tokens if word not in self.all_stopwords]
    
    def apply_stemming(self, tokens: List[str]) -> List[str]:

        stemmed = []
        suffix_rules = [
            ('amentos', 'ament'), ('amentos', 'ament'), ('amento', 'ament'),
            ('ências', 'ênci'), ('ência', 'ênci'), ('entes', 'ent'),
            ('ente', 'ent'), ('ações', 'ação'), ('ação', 'ação'),
            ('adores', 'ador'), ('ador', 'ador'), ('istas', 'ist'),
            ('ista', 'ist'), ('ismos', 'ism'), ('ismo', 'ism'),
            ('adas', 'ad'), ('ada', 'ad'), ('idos', 'id'), ('ido', 'id'),
            ('adas', 'ad'), ('ada', 'ad'), ('idos', 'id'), ('ido', 'id'),
            ('entes', 'ent'), ('ente', 'ent'), ('ões', 'ão'), ('ão', 'ão'),
            ('s', ''), ('es', 'e'), ('is', 'il'), ('ns', 'n'),
        ]
        
        for token in tokens:
            stemmed_token = token
            for suffix, replacement in suffix_rules:
                if token.endswith(suffix):
                    stemmed_token = token[:-len(suffix)] + replacement
                    break
            stemmed.append(stemmed_token)
        
        return stemmed
    
    def full_preprocess(self, text: str, return_tokens: bool = False) -> str:

        if not text or len(text.strip()) < 10:
            return "" if not return_tokens else []
        
        print(f"[NLP] Texto original ({len(text)} chars): {text[:100]}...")
        
        normalized = self.normalize_text(text)
        print(f"[NLP] Após normalização: {normalized[:100]}...")
        
        tokens = self.tokenize_words(normalized)
        print(f"[NLP] Tokens brutos ({len(tokens)}): {tokens[:10]}...")
        
        tokens_no_stopwords = self.remove_stopwords(tokens)
        print(f"[NLP] Tokens sem stopwords ({len(tokens_no_stopwords)}): {tokens_no_stopwords[:10]}...")
        
        stemmed_tokens = self.apply_stemming(tokens_no_stopwords)
        print(f"[NLP] Tokens com stemming ({len(stemmed_tokens)}): {stemmed_tokens[:10]}...")
        
        if return_tokens:
            return stemmed_tokens
        else:
            processed_text = ' '.join(stemmed_tokens)
            print(f"[NLP] Texto final ({len(processed_text)} chars): {processed_text[:100]}...")
            return processed_text

nlp_processor = NLPProcessor()

def preprocess_email_text(text: str) -> str:
    return nlp_processor.full_preprocess(text)

def get_email_keywords(text: str, top_n: int = 15) -> List[Tuple[str, int]]:
    processed_tokens = nlp_processor.full_preprocess(text, return_tokens=True)
    freq_dist = Counter(processed_tokens)
    return freq_dist.most_common(top_n)

if __name__ == "__main__":
    print("✅ NLP PROCESSOR SIMPLIFICADO - PRONTO PARA USO")
    print("=" * 60)
    
    test_text = "Prezados, tenho um problema urgente com pagamentos no sistema."
    result = preprocess_email_text(test_text)
    print(f"Teste: '{test_text}'")
    print(f"Resultado: '{result}'")