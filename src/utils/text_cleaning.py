import re
import unicodedata

def normalize_unicode(text: str) -> str:
    """Normalize unicode (NFC)."""
    return unicodedata.normalize("NFC", text)

def standardize_punctuation(text: str) -> str:
    """Standardize punctuation and symbols."""
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "…": "...",
        "•": "-", "●": "-", "·": "-"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def remove_noise(text: str) -> str:
    """Remove headers, footers, page numbers, extra spaces."""

    text = re.sub(r"\n?\s*\d+\s*\n", "\n", text)

    text = re.sub(r"\n{2,}", "\n", text)

    text = re.sub(r"\s{2,}", " ", text)

    text = re.sub(r"([!?.]){2,}", r"\1", text)

    return text.strip()

def fix_linebreaks(text: str) -> str:
    """Fix broken words split by hyphenation at line breaks."""
    return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

def clean_text(text: str) -> str:
    """
    Full cleaning pipeline:
    1. Unicode normalization
    2. Punctuation standardization
    3. Noise removal
    4. Linebreak fixes
    """
    text = normalize_unicode(text)
    text = standardize_punctuation(text)
    text = fix_linebreaks(text)
    text = remove_noise(text)

    return text.lower()
