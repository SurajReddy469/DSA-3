import re
from typing import Dict, Any, List
from app.preprocessing.tokenizer import Tokenizer


class ParsedQuery:
    """
    Structured representation of a parsed user query.
    """
    def __init__(self, operator: str, terms: List[str], raw_query: str):
        self.operator: str = operator.upper()  # 'AND', 'OR', 'SINGLE', 'PHRASE'
        self.terms: List[str] = terms
        self.raw_query: str = raw_query

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operator": self.operator,
            "terms": self.terms,
            "raw_query": self.raw_query
        }


class QueryParser:
    """
    Parses user input query strings into structured ParsedQuery objects.
    Supports single keyword, multi-keyword AND, multi-keyword OR, and phrase queries.
    """

    def __init__(self):
        self.tokenizer = Tokenizer()

    def parse(self, raw_query: str, default_mode: str = "AND") -> ParsedQuery:
        if not raw_query or not raw_query.strip():
            return ParsedQuery(operator="SINGLE", terms=[], raw_query="")

        clean_query = raw_query.strip()

        # Check for phrase query
        if clean_query.startswith('"') and clean_query.endswith('"') and len(clean_query) > 2:
            inner_text = clean_query[1:-1]
            terms = self.tokenizer.tokenize(inner_text)
            return ParsedQuery(operator="PHRASE", terms=terms, raw_query=clean_query)

        # Extract search terms using Unicode Tokenizer
        all_terms = self.tokenizer.tokenize(clean_query)
        filtered_terms = [t for t in all_terms if t not in ("and", "or")]

        if not filtered_terms:
            filtered_terms = all_terms

        if len(filtered_terms) == 1:
            operator = "SINGLE"
        else:
            tokens = clean_query.split()
            upper_tokens = [t.upper() for t in tokens]
            if "AND" in upper_tokens:
                operator = "AND"
            elif "OR" in upper_tokens:
                operator = "OR"
            else:
                operator = default_mode.upper()

        return ParsedQuery(operator=operator, terms=filtered_terms, raw_query=clean_query)
