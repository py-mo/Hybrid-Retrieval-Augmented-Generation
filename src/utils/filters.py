import spacy

nlp = spacy.load("en_core_web_sm")

def language_filter(text: str, target_lang="en") -> bool:
    """
    Basic language check.
    """
    if target_lang == "en":
        doc = nlp(text=text)
        tokens = [t.text for t in doc if t.is_alpha]
        return len(tokens) > (len(text) / 2)
    return True

def stopword_filter(text: str) -> bool:
    """
    Return True if text is meaningful.
    """
    doc = nlp(text)
    tokens = [t for t in doc if t.is_alpha]

    stopword_ratio = sum(1 for t in tokens if t.is_stop) / len(tokens)
    if stopword_ratio > 0.2:
        return False
    return True

def filter_segments(segments, lang="en"):
    """
    Apply all filters to a list of text segments.
    Returns only relevant ones.
    """
    filtered = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        if not language_filter(seg, lang):
            continue
        if not stopword_filter(seg):
            continue
        filtered.append(seg)
    return filtered
