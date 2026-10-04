import re
from app.preprocessing.unicode_utils import normalize_unicode


class TextCleaner:
    """
    Cleans raw document text, removing HTML, Wiki markup, URLs, and excess whitespace,
    while carefully preserving Unicode characters of Indian scripts.
    """

    def __init__(self):
        # Regex patterns
        self.html_pattern = re.compile(r'<[^>]+>')
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self.wiki_link_pattern = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
        self.wiki_template_pattern = re.compile(r'\{\{[^}]+\}\}')
        self.wiki_header_pattern = re.compile(r'=+([^=]+)=+')
        # Remove common ASCII punctuation but retain words and Indian Unicode characters
        self.punct_pattern = re.compile(r'[!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~–—’“”«»]')
        self.whitespace_pattern = re.compile(r'\s+')

    def clean(self, text: str) -> str:
        """
        Cleans input string in sequential steps.
        Complexity: O(N) where N is text length.
        """
        if not text:
            return ""

        # Step 1: Unicode Normalization (NFC)
        text = normalize_unicode(text, form="NFC")

        # Step 2: Remove URLs
        text = self.url_pattern.sub(' ', text)

        # Step 3: Remove HTML tags
        text = self.html_pattern.sub(' ', text)

        # Step 4: Clean Wikipedia markup
        text = self.wiki_template_pattern.sub(' ', text)
        text = self.wiki_link_pattern.sub(r'\1', text)
        text = self.wiki_header_pattern.sub(r'\1', text)

        # Step 5: Remove punctuation
        text = self.punct_pattern.sub(' ', text)

        # Step 6: Normalize whitespace
        text = self.whitespace_pattern.sub(' ', text).strip()

        return text
