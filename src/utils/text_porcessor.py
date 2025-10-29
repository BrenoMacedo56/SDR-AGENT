import re

def clean_text(text: str) -> str:
    """Remove espaços duplicados, caracteres estranhos e normaliza texto."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9À-ÿ@.\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(text: str, keywords: list[str]) -> list[str]:
    """Retorna palavras-chave encontradas no texto."""
    text = text.lower()
    return [k for k in keywords if k.lower() in text]