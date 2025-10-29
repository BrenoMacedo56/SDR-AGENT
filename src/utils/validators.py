import re

def is_valid_email(email: str) -> bool:
    """Valida formato de e-mail."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def is_valid_phone(phone: str) -> bool:
    """Valida formato de telefone brasileiro simples."""
    pattern = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
    return bool(re.match(pattern, phone.strip()))

def is_valid_name(name: str) -> bool:
    """Valida nome (mínimo 2 palavras e sem números)."""
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(\s[A-Za-zÀ-ÖØ-öø-ÿ]+)+$", name.strip()))