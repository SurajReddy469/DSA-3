import unicodedata
from typing import Dict, Optional

# Indic Unicode Blocks Mapping
INDIC_UNICODE_BLOCKS: Dict[str, tuple] = {
    "Devanagari": (0x0900, 0x097F),  # Hindi, Marathi
    "Bengali": (0x0980, 0x09FF),     # Bengali
    "Gurmukhi": (0x0A00, 0x0A7F),    # Punjabi
    "Gujarati": (0x0A80, 0x0AFF),    # Gujarati
    "Oriya": (0x0B00, 0x0B7F),       # Odia
    "Tamil": (0x0B80, 0x0BFF),       # Tamil
    "Telugu": (0x0C00, 0x0C7F),      # Telugu
    "Kannada": (0x0C80, 0x0CFF),     # Kannada
    "Malayalam": (0x0D00, 0x0D7F),   # Malayalam
}


def normalize_unicode(text: str, form: str = "NFC") -> str:
    """
    Applies Unicode normalization (default NFC) to preserve multi-grapheme
    Indian language characters without splitting combining marks or diacritics.

    Complexity: O(N) where N is string length in characters.
    """
    if not text:
        return ""
    return unicodedata.normalize(form, text)


def is_indic_character(char: str) -> bool:
    """
    Checks if a character falls within any recognized Indian script Unicode range.
    """
    cp = ord(char)
    for block_name, (start, end) in INDIC_UNICODE_BLOCKS.items():
        if start <= cp <= end:
            return True
    return False


def detect_primary_script(text: str) -> Optional[str]:
    """
    Detects the primary Indic script present in the given text string.
    Returns script name (e.g. 'Telugu', 'Devanagari') or None if non-Indic/English.
    """
    counts = {script: 0 for script in INDIC_UNICODE_BLOCKS}
    for char in text:
        cp = ord(char)
        for script, (start, end) in INDIC_UNICODE_BLOCKS.items():
            if start <= cp <= end:
                counts[script] += 1
                break
    
    max_script = max(counts.items(), key=lambda x: x[1])
    if max_script[1] > 0:
        return max_script[0]
    return "Latin/Other"
