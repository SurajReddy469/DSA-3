import re
from typing import List, Set
from app.preprocessing.unicode_utils import normalize_unicode


DEFAULT_TELUGU_STOPWORDS: Set[str] = {
    "అని", "మరియు", "కూడా", "ఈ", "ఆ", "ఒక", "అనే", "లేదా", "అందుకే", "దీనిని",
    "వారి", "తన", "తనను", "ఉంది", "ఉన్నాయి", "చేసి", "చేసే", "ద్వారా", "వల్ల"
}

DEFAULT_ENGLISH_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "in", "on", "at", "of", "to", "is", "are", "was", "were", "for", "with"
}


class Tokenizer:
    """
    Unicode-aware Tokenizer abstraction for Indian-language and multilingual text.
    Preserves Indic letters, combining vowel marks (Mn, Mc), virama, anusvara, and ZWJ/ZWNJ intact.
    """

    def __init__(self, remove_stopwords: bool = False, stopwords: Set[str] = None):
        # Match tokens consisting of word characters, Indic script blocks, and combining marks
        # Excluding whitespace and standard punctuation.
        self.word_token_pattern = re.compile(
            r'[^\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~–—’“”«»।॥]+',
            re.UNICODE
        )
        self.remove_stopwords = remove_stopwords
        self.stopwords = stopwords or (DEFAULT_TELUGU_STOPWORDS | DEFAULT_ENGLISH_STOPWORDS)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes text into a list of cleaned, normalized Unicode term tokens.
        Complexity: O(N) where N is length of text.
        """
        if not text:
            return []

        norm_text = normalize_unicode(text, form="NFC")
        raw_tokens = self.word_token_pattern.findall(norm_text)

        processed_tokens: List[str] = []
        for token in raw_tokens:
            token_clean = token.strip()
            # Lowercase Latin characters while keeping Indic glyphs intact
            token_lower = token_clean.lower()
            if self.remove_stopwords and token_lower in self.stopwords:
                continue
            if len(token_lower) > 0:
                processed_tokens.append(token_lower)

        return processed_tokens
