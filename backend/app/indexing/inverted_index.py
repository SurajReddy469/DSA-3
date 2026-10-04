import pickle
import json
import time
from pathlib import Path
from typing import Dict, Optional, Any, List
from app.indexing.posting_list import PostingList, Posting


class InvertedIndex:
    """
    Inverted Index Data Structure for Indian-Language Wikipedia Text Analytics.

    Dictionary structure:
    TERM (str) -> POSTING LIST (PostingList object)

    Complexity Analysis:
    - Term Lookup: Average O(1) via hash table dictionary lookup.
    - Term Insertion during Indexing: Average O(1) per term instance.
    - Index Loading/Saving: O(V + N) where V is unique terms and N is total postings.
    """

    def __init__(self):
        # Primary Hash Table: term (str) -> PostingList
        self.term_dict: Dict[str, PostingList] = {}
        # Document Metadata: doc_id -> metadata dict (title, language, text, source)
        self.doc_metadata: Dict[int, Dict[str, Any]] = {}
        # Document Lengths: doc_id -> total token count
        self.doc_lengths: Dict[int, int] = {}
        # Index build metadata
        self.total_documents: int = 0
        self.total_tokens: int = 0
        self.build_time_sec: float = 0.0

    def add_document(self, doc_id: int, tokens: List[str], metadata: Dict[str, Any]):
        """
        Adds a preprocessed document into the inverted index.
        """
        self.doc_metadata[doc_id] = metadata
        doc_len = len(tokens)
        self.doc_lengths[doc_id] = doc_len
        self.total_tokens += doc_len
        self.total_documents += 1

        # Track term frequencies and positions within the document
        term_positions: Dict[str, List[int]] = {}
        for pos, term in enumerate(tokens):
            if term not in term_positions:
                term_positions[term] = []
            term_positions[term].append(pos)

        # Update posting lists in the hash table
        for term, positions in term_positions.items():
            if term not in self.term_dict:
                self.term_dict[term] = PostingList()
            self.term_dict[term].add_posting(
                doc_id=doc_id,
                tf=len(positions),
                position=None # Store length directly to save RAM; positions preserved in list if needed
            )

    def get_postings(self, term: str) -> Optional[PostingList]:
        """
        Retrieves posting list for a term in O(1) average time.
        """
        return self.term_dict.get(term)

    def get_doc_frequency(self, term: str) -> int:
        """
        Returns document frequency DF(term).
        """
        plist = self.term_dict.get(term)
        return plist.df if plist else 0

    def get_avg_doc_length(self) -> float:
        """
        Returns average document length across corpus.
        """
        if self.total_documents == 0:
            return 0.0
        return self.total_tokens / self.total_documents

    def get_stats(self) -> Dict[str, Any]:
        """
        Calculates index statistics.
        """
        unique_terms = len(self.term_dict)
        max_plist_len = max((plist.df for plist in self.term_dict.values()), default=0)
        
        # Language distribution
        lang_counts: Dict[str, int] = {}
        for meta in self.doc_metadata.values():
            lang = meta.get("language", "unknown")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        # Top 20 most frequent terms
        term_df_list = [
            {"term": term, "df": plist.df, "total_tf": sum(p.tf for p in plist)}
            for term, plist in self.term_dict.items()
        ]
        term_df_list.sort(key=lambda x: x["df"], reverse=True)
        top_20 = term_df_list[:20]

        return {
            "total_documents": self.total_documents,
            "total_tokens": self.total_tokens,
            "unique_terms": unique_terms,
            "avg_tokens_per_doc": round(self.get_avg_doc_length(), 2),
            "max_posting_list_len": max_plist_len,
            "index_build_time_sec": round(self.build_time_sec, 3),
            "languages_supported": lang_counts,
            "top_20_terms": top_20
        }

    def save_index(self, filepath: Path, metadata_path: Optional[Path] = None):
        """
        Serializes the index to disk using pickle.
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        if metadata_path:
            stats = self.get_stats()
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_index(cls, filepath: Path) -> 'InvertedIndex':
        """
        Deserializes index from disk.
        """
        with open(filepath, 'rb') as f:
            index_obj = pickle.load(f)
        return index_obj
