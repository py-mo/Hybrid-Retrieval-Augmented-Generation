import spacy
from typing import List, Optional

class FilterError(Exception):
    """Custom exception for filtering errors"""
    pass

try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise FilterError("Failed to load spaCy model: en_core_web_sm. Please ensure it's installed.")

def language_filter(text: str) -> bool:
    try:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
            
        if not text.strip():
            return False
            
        doc = nlp(text)
        
        valid_tokens = [token for token in doc if token.is_alpha and not token.is_punct and not token.like_num]
        if not valid_tokens:
            return False
        
        recognized_ratio = sum(1 for token in valid_tokens if token.lemma_ != "-PRON-" and token.has_vector) / len(valid_tokens)
        
        return recognized_ratio > 0.6
        
    except Exception as e:
        raise FilterError(f"Language filter failed: {str(e)}")

def stopword_filter(text: str) -> bool:
    try:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
            
        if not text.strip():
            return False
            
        doc = nlp(text)
        tokens = [t for t in doc if t.is_alpha]
        
        if not tokens:
            return False
            
        stopword_ratio = sum(1 for t in tokens if t.is_stop) / len(tokens)
        return stopword_ratio <= 0.2
        
    except Exception as e:
        raise FilterError(f"Stopword filter failed: {str(e)}")

def filter_segments(segments: List[str]) -> List[str]:
    """
    Args:
        segments (List[str]): List of text segments to filter
        
    Returns:
        List[str]: List of filtered segments that pass all criteria
        
    Raises:
        FilterError: If filtering process fails
        TypeError: If input is not a list of strings
    """
    try:
        if not isinstance(segments, list):
            raise TypeError("Input must be a list of strings")
            
        filtered = []
        for seg in segments:
            try:
                if not isinstance(seg, str):
                    continue
                    
                seg = seg.strip()
                if not seg:
                    continue
                    
                if not language_filter(seg):
                    continue
                    
                if not stopword_filter(seg):
                    continue
                    
                filtered.append(seg)
                
            except FilterError as e:
                print(f"Error processing segment: {str(e)}")
                continue
                
        return filtered
        
    except Exception as e:
        raise FilterError(f"Segment filtering failed: {str(e)}")
