import re

def clean_text(text: str) -> str:
    """
    Lowercase, remove special chars, multiple spaces.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()