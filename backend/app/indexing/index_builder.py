import json
import time
from pathlib import Path
from typing import List, Dict, Any
from app.indexing.inverted_index import InvertedIndex
from app.preprocessing.cleaner import TextCleaner
from app.preprocessing.tokenizer import Tokenizer
from app.config import RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH


class IndexBuilder:
    """
    Pipeline orchestrator that takes raw or preprocessed corpus documents,
    applies cleaning & Unicode tokenization, constructs the inverted index,
    and serializes it to disk.
    """

    def __init__(self, remove_stopwords: bool = False):
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer(remove_stopwords=remove_stopwords)

    def build_from_documents(self, documents: List[Dict[str, Any]]) -> InvertedIndex:
        """
        Builds InvertedIndex from list of document dictionaries.
        Each doc dict must contain 'document_id', 'title', 'language', 'text', 'source'.

        Complexity Analysis:
        - Time: O(D * L) where D is number of documents and L is avg tokens per document.
        - Space: O(V + N) where V is vocabulary size and N is total term postings.
        """
        index = InvertedIndex()
        start_time = time.perf_counter()

        for doc in documents:
            doc_id = int(doc["document_id"])
            raw_text = doc.get("text", "")
            title = doc.get("title", "")
            
            # Clean text
            cleaned_text = self.cleaner.clean(raw_text)
            
            # Tokenize title + text to ensure title terms are indexed
            full_content = f"{title} {cleaned_text}"
            tokens = self.tokenizer.tokenize(full_content)
            
            metadata = {
                "document_id": doc_id,
                "title": title,
                "language": doc.get("language", "te"),
                "source": doc.get("source", "Wikipedia"),
                "text": raw_text[:300] + "..." if len(raw_text) > 300 else raw_text
            }
            
            index.add_document(doc_id=doc_id, tokens=tokens, metadata=metadata)

        index.build_time_sec = time.perf_counter() - start_time
        return index

    def build_from_file(self, corpus_path: Path = RAW_CORPUS_PATH) -> InvertedIndex:
        """
        Loads corpus JSON from file system and builds index.
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        return self.build_from_documents(documents)


def build_and_save_index(corpus_path: Path = RAW_CORPUS_PATH, index_path: Path = INDEX_FILE_PATH, metadata_path: Path = INDEX_METADATA_PATH) -> InvertedIndex:
    """
    Helper script entry point.
    """
    builder = IndexBuilder()
    index = builder.build_from_file(corpus_path)
    index.save_index(index_path, metadata_path)
    return index
