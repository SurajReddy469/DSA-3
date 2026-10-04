import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import RAW_CORPUS_PATH, INDEX_FILE_PATH
from app.indexing.inverted_index import InvertedIndex
from app.evaluation.benchmark import PerformanceBenchmark


def main():
    print("Running Search Engine Performance Benchmarks...")
    if not INDEX_FILE_PATH.exists():
        print("Index file not found! Run build_index.py first.")
        sys.exit(1)

    index = InvertedIndex.load_index(INDEX_FILE_PATH)
    
    with open(RAW_CORPUS_PATH, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    benchmarker = PerformanceBenchmark(full_index=index, documents=documents)
    
    test_queries = ["కంప్యూటర్", "కృత్రిమ మేధస్సు", "సాంకేతిక పరిజ్ఞానం"]
    
    for query in test_queries:
        print(f"\nEvaluating Query: '{query}'")
        res = benchmarker.run_benchmark(query=query, sample_sizes=[500, 1000, 2500, 5000], runs_per_size=3)
        
        print(f"{'Doc Count':<12} | {'Naive Time (ms)':<18} | {'Indexed Time (ms)':<18} | {'Speedup':<10} | {'Results'}")
        print("-" * 75)
        for item in res["benchmarks"]:
            print(f"{item['dataset_size']:<12} | {item['naive_time_ms']:<18.3f} | {item['indexed_time_ms']:<18.3f} | {item['speedup_factor']:<10.2f}x | {item['results_count']}")


if __name__ == "__main__":
    main()
