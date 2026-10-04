import re
import time
from typing import Dict, List, Any, Optional
from app.indexing.inverted_index import InvertedIndex
from app.indexing.posting_list import PostingList, intersect_postings, union_postings
from app.search.query_parser import QueryParser, ParsedQuery
from app.search.ranking import FrequencyRanker, TFIDFRanker
from app.preprocessing.cleaner import TextCleaner
from app.preprocessing.tokenizer import Tokenizer
from app.config import DEFAULT_SNIPPET_LENGTH


class SearchEngine:
    """
    Core Search Engine unifying Inverted-Index search, Naive baseline search,
    Snippet Generation, and Result Filtering.
    """

    def __init__(self, index: InvertedIndex):
        self.index = index
        self.query_parser = QueryParser()
        self.freq_ranker = FrequencyRanker()
        self.tfidf_ranker = TFIDFRanker()
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer()

    def search_indexed(
        self,
        query_str: str,
        mode: str = "AND",
        ranking: str = "tfidf",
        language: Optional[str] = "all",
        limit: int = 10,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Executes search using the Inverted Index posting lists and two-pointer operations.

        Complexity Analysis:
        - Query Parsing: O(|Q|)
        - Hash Table Lookup: O(1) per term
        - Two-Pointer Intersection/Union: O(|A| + |B|)
        - Candidate Scoring & Ranking: O(C log C) where C is candidate document count
        - Total Time: Millisecond / Sub-millisecond scale
        """
        start_time = time.perf_counter()

        parsed_query: ParsedQuery = self.query_parser.parse(query_str, default_mode=mode)
        query_terms = parsed_query.terms

        if not query_terms:
            return {
                "query": query_str,
                "mode": mode,
                "ranking": ranking,
                "total_results": 0,
                "search_time_ms": round((time.perf_counter() - start_time) * 1000.0, 3),
                "results": [],
                "page": page,
                "limit": limit,
                "total_pages": 0
            }

        # 1. Fetch posting lists for terms from hash table dictionary
        posting_lists: List[PostingList] = []
        term_map: Dict[str, PostingList] = {}

        for term in query_terms:
            plist = self.index.get_postings(term)
            if plist:
                posting_lists.append(plist)
                term_map[term] = plist

        if not posting_lists:
            return {
                "query": query_str,
                "mode": mode,
                "ranking": ranking,
                "total_results": 0,
                "search_time_ms": round((time.perf_counter() - start_time) * 1000.0, 3),
                "results": [],
                "page": page,
                "limit": limit,
                "total_pages": 0
            }

        # 2. Perform Posting List Operations (Intersection or Union)
        eff_mode = parsed_query.operator
        if eff_mode in ("AND", "SINGLE", "PHRASE"):
            final_plist = posting_lists[0]
            for plist in posting_lists[1:]:
                final_plist = intersect_postings(final_plist, plist)
        else:  # OR mode
            final_plist = posting_lists[0]
            for plist in posting_lists[1:]:
                final_plist = union_postings(final_plist, plist)

        # 3. Collect Candidate Documents and Term Frequencies
        candidates: Dict[int, Dict[str, Any]] = {}
        for posting in final_plist.get_postings():
            doc_id = posting.doc_id
            
            # Language filter
            if language and language != "all":
                doc_lang = self.index.doc_metadata.get(doc_id, {}).get("language")
                if doc_lang != language:
                    continue

            # Calculate individual term freqs in this candidate document
            term_freqs: Dict[str, int] = {}
            matched_terms: List[str] = []

            for term in query_terms:
                plist = term_map.get(term)
                if plist:
                    for p in plist.get_postings():
                        if p.doc_id == doc_id:
                            term_freqs[term] = p.tf
                            matched_terms.append(term)
                            break

            candidates[doc_id] = {
                "term_freqs": term_freqs,
                "matched_terms": matched_terms
            }

        # 4. Rank Candidates
        if ranking.lower() == "frequency":
            ranked_docs = self.freq_ranker.rank(candidates, self.index, query_terms)
        else:
            ranked_docs = self.tfidf_ranker.rank(candidates, self.index, query_terms)

        total_results = len(ranked_docs)
        total_pages = (total_results + limit - 1) // limit if limit > 0 else 1

        # 5. Pagination & Snippet Generation
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paged_docs = ranked_docs[start_idx:end_idx]

        final_results = []
        for doc in paged_docs:
            snippet = self.generate_snippet(doc["text"], doc["matched_terms"])
            doc["snippet"] = snippet
            # Exclude raw full text from HTTP payload size
            del doc["text"]
            final_results.append(doc)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "query": query_str,
            "mode": eff_mode,
            "ranking": ranking,
            "total_results": total_results,
            "search_time_ms": round(elapsed_ms, 3),
            "results": final_results,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    def search_naive(
        self,
        query_str: str,
        mode: str = "AND",
        ranking: str = "tfidf",
        language: Optional[str] = "all",
        limit: int = 10,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Baseline Naive Search scanning all raw corpus documents linearly.
        Used strictly for empirical performance benchmark comparisons.

        Complexity: O(N * L) where N is total document count and L is doc length.
        """
        start_time = time.perf_counter()

        parsed_query = self.query_parser.parse(query_str, default_mode=mode)
        query_terms = set(parsed_query.terms)

        if not query_terms:
            return {
                "query": query_str,
                "mode": mode,
                "ranking": ranking,
                "total_results": 0,
                "search_time_ms": round((time.perf_counter() - start_time) * 1000.0, 3),
                "results": [],
                "page": page,
                "limit": limit,
                "total_pages": 0
            }

        candidates: Dict[int, Dict[str, Any]] = {}

        # Linear scan over all doc_metadata in the corpus
        for doc_id, meta in self.index.doc_metadata.items():
            if language and language != "all" and meta.get("language") != language:
                continue

            full_text = f"{meta.get('title', '')} {meta.get('text', '')}"
            doc_tokens = self.tokenizer.tokenize(full_text)

            term_freqs: Dict[str, int] = {}
            for token in doc_tokens:
                if token in query_terms:
                    term_freqs[token] = term_freqs.get(token, 0) + 1

            matched_terms = list(term_freqs.keys())

            # Evaluate query match condition
            if parsed_query.operator in ("AND", "SINGLE", "PHRASE"):
                is_match = len(matched_terms) == len(query_terms)
            else:  # OR mode
                is_match = len(matched_terms) > 0

            if is_match:
                candidates[doc_id] = {
                    "term_freqs": term_freqs,
                    "matched_terms": matched_terms
                }

        # Rank
        if ranking.lower() == "frequency":
            ranked_docs = self.freq_ranker.rank(candidates, self.index, list(query_terms))
        else:
            ranked_docs = self.tfidf_ranker.rank(candidates, self.index, list(query_terms))

        total_results = len(ranked_docs)
        total_pages = (total_results + limit - 1) // limit if limit > 0 else 1

        start_idx = (page - 1) * limit
        paged_docs = ranked_docs[start_idx:start_idx + limit]

        final_results = []
        for doc in paged_docs:
            snippet = self.generate_snippet(doc["text"], doc["matched_terms"])
            doc["snippet"] = snippet
            del doc["text"]
            final_results.append(doc)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "query": query_str,
            "mode": mode,
            "ranking": ranking,
            "total_results": total_results,
            "search_time_ms": round(elapsed_ms, 3),
            "results": final_results,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    def generate_snippet(self, text: str, matched_terms: List[str], max_len: int = DEFAULT_SNIPPET_LENGTH) -> str:
        """
        Generates a snippet centered around the first occurrence of a matched term.
        Applies HTML highlight markers <mark>term</mark> for UI presentation.
        """
        if not text:
            return ""

        clean_text = self.cleaner.clean(text)
        if not matched_terms:
            return clean_text[:max_len] + "..." if len(clean_text) > max_len else clean_text

        # Find earliest match index
        first_match_idx = -1
        first_term = ""
        lower_text = clean_text.lower()

        for term in matched_terms:
            idx = lower_text.find(term.lower())
            if idx != -1 and (first_match_idx == -1 or idx < first_match_idx):
                first_match_idx = idx
                first_term = term

        if first_match_idx == -1:
            snippet = clean_text[:max_len]
        else:
            half = max_len // 2
            start = max(0, first_match_idx - half)
            end = min(len(clean_text), start + max_len)
            
            # Adjust start if end hit string boundary
            if end - start < max_len:
                start = max(0, end - max_len)
                
            snippet = clean_text[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(clean_text):
                snippet = snippet + "..."

        # Apply term highlighting markers
        for term in matched_terms:
            if term and len(term) > 1:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                snippet = pattern.sub(r'<mark>\g<0></mark>', snippet)

        return snippet
