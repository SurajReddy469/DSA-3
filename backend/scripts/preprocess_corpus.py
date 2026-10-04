import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import RAW_CORPUS_PATH, PROCESSED_CORPUS_PATH
from app.preprocessing.cleaner import TextCleaner
from app.preprocessing.tokenizer import Tokenizer


def preprocess():
    print(f"Reading raw corpus from {RAW_CORPUS_PATH}...")
    if not RAW_CORPUS_PATH.exists():
        print("Raw corpus file not found! Run generate_sample_dataset.py first.")
        sys.exit(1)

    with open(RAW_CORPUS_PATH, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    cleaner = TextCleaner()
    tokenizer = Tokenizer()
    processed_docs = []

    print("Preprocessing text, cleaning Unicode markup, and generating token lists...")
    for doc in documents:
        clean_text = cleaner.clean(doc.get("text", ""))
        tokens = tokenizer.tokenize(f"{doc.get('title', '')} {clean_text}")
        
        processed_doc = {
            "document_id": doc["document_id"],
            "title": doc["title"],
            "language": doc["language"],
            "cleaned_text": clean_text,
            "token_count": len(tokens),
            "tokens": tokens,
            "source": doc.get("source", "Wikipedia Sample")
        }
        processed_docs.append(processed_doc)

    PROCESSED_CORPUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_CORPUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(processed_docs, f, ensure_ascii=False, indent=2)

    print(f"Preprocessed {len(processed_docs)} documents saved to {PROCESSED_CORPUS_PATH}")


if __name__ == "__main__":
    preprocess()
