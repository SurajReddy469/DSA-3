import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH
from app.indexing.index_builder import build_and_save_index


def main():
    print("Building Inverted Index from corpus...")
    start_time = time.perf_counter()
    
    if not RAW_CORPUS_PATH.exists():
        print("Raw corpus file not found! Generating sample dataset now...")
        from scripts.generate_sample_dataset import main as gen_main
        gen_main()

    index = build_and_save_index(RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH)
    elapsed = time.perf_counter() - start_time
    
    stats = index.get_stats()
    print("\n--- INVERTED INDEX BUILD SUMMARY ---")
    print(f"Total Documents Indexed : {stats['total_documents']}")
    print(f"Total Tokens Processed  : {stats['total_tokens']}")
    print(f"Unique Vocabulary Terms : {stats['unique_terms']}")
    print(f"Avg Tokens/Document     : {stats['avg_tokens_per_doc']}")
    print(f"Max Posting List Length : {stats['max_posting_list_len']}")
    print(f"Index Build Time        : {elapsed:.3f} seconds")
    print(f"Index File Saved        : {INDEX_FILE_PATH}")
    print(f"Metadata File Saved     : {INDEX_METADATA_PATH}")
    print("------------------------------------\n")


if __name__ == "__main__":
    main()
