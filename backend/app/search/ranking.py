import math
from typing import Dict, List, Tuple, Any
from app.indexing.inverted_index import InvertedIndex


class BaseRanker:
    """Base class for ranking candidate search documents."""
    def rank(self, candidates: Dict[int, Dict[str, Any]], index: InvertedIndex, query_terms: List[str]) -> List[Dict[str, Any]]:
        raise NotImplementedError


class FrequencyRanker(BaseRanker):
    """
    Frequency-Based Ranking Algorithm.
    Scores each candidate document by the total occurrence count of all matched query terms.

    Score formula:
    score(d) = sum(tf(t, d) for t in query_terms)

    Complexity: O(C * |Q|) where C is number of candidate documents and |Q| is query terms count.
    """

    def rank(self, candidates: Dict[int, Dict[str, Any]], index: InvertedIndex, query_terms: List[str]) -> List[Dict[str, Any]]:
        scored_docs = []

        for doc_id, data in candidates.items():
            matched_terms = data.get("matched_terms", [])
            term_freqs = data.get("term_freqs", {})

            # Total occurrences of query terms in document
            total_occurrences = sum(term_freqs.values())
            score = float(total_occurrences)

            metadata = index.doc_metadata.get(doc_id, {})

            scored_docs.append({
                "document_id": doc_id,
                "title": metadata.get("title", f"Doc #{doc_id}"),
                "language": metadata.get("language", "te"),
                "source": metadata.get("source", "Wikipedia Sample"),
                "text": metadata.get("text", ""),
                "score": round(score, 2),
                "occurrences": total_occurrences,
                "matched_terms": matched_terms,
                "ranking_method": "frequency"
            })

        # Sort descending by score, then doc_id
        scored_docs.sort(key=lambda x: (x["score"], x["occurrences"]), reverse=True)
        return scored_docs


class TFIDFRanker(BaseRanker):
    """
    TF-IDF (Term Frequency - Inverse Document Frequency) Ranking Algorithm.

    Formulas:
    - Term Frequency (TF):
        TF(t, d) = tf(t, d) / |d|   (Normalized by document token length)
    - Inverse Document Frequency (IDF):
        IDF(t) = log((N + 1) / (DF(t) + 1)) + 1
    - TF-IDF Score:
        Score(d) = sum(TF(t, d) * IDF(t) for t in query_terms)

    Complexity: O(C * |Q|) where C is candidate docs count and |Q| is query terms count.
    """

    def rank(self, candidates: Dict[int, Dict[str, Any]], index: InvertedIndex, query_terms: List[str]) -> List[Dict[str, Any]]:
        scored_docs = []
        N = index.total_documents

        if N == 0:
            return []

        # Precompute IDF for each query term
        idf_values: Dict[str, float] = {}
        for term in query_terms:
            df = index.get_doc_frequency(term)
            if df > 0:
                idf = math.log((N + 1.0) / (df + 1.0)) + 1.0
            else:
                idf = 0.0
            idf_values[term] = idf

        for doc_id, data in candidates.items():
            term_freqs = data.get("term_freqs", {})
            matched_terms = data.get("matched_terms", [])
            doc_len = index.doc_lengths.get(doc_id, 1)

            total_occurrences = sum(term_freqs.values())
            tfidf_score = 0.0

            for term, tf in term_freqs.items():
                if term in idf_values:
                    # Normalized TF
                    tf_norm = tf / max(doc_len, 1)
                    tfidf_score += tf_norm * idf_values[term]

            metadata = index.doc_metadata.get(doc_id, {})

            scored_docs.append({
                "document_id": doc_id,
                "title": metadata.get("title", f"Doc #{doc_id}"),
                "language": metadata.get("language", "te"),
                "source": metadata.get("source", "Wikipedia Sample"),
                "text": metadata.get("text", ""),
                "score": round(tfidf_score * 100.0, 4),  # Scale for display readability
                "occurrences": total_occurrences,
                "matched_terms": matched_terms,
                "ranking_method": "tfidf"
            })

        scored_docs.sort(key=lambda x: (x["score"], x["occurrences"]), reverse=True)
        return scored_docs
