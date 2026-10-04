import time
from typing import List, Dict, Any
from app.indexing.inverted_index import InvertedIndex
from app.indexing.index_builder import IndexBuilder
from app.search.search_engine import SearchEngine
from app.evaluation.metrics import calculate_speedup


class PerformanceBenchmark:
    """
    Empirical Benchmark Suite comparing Naive Baseline Search against Inverted Index Search.
    Executes actual high-resolution timing trials across varying corpus slice sizes.
    """

    def __init__(self, full_index: InvertedIndex, documents: List[Dict[str, Any]]):
        self.full_index = full_index
        self.documents = documents

    def run_benchmark(
        self,
        query: str = "కంప్యూటర్",
        sample_sizes: List[int] = None,
        runs_per_size: int = 3
    ) -> Dict[str, Any]:
        """
        Executes benchmarks across specified document subset sizes.
        Returns empirical search timings and speedup ratios.
        """
        if sample_sizes is None:
            total_docs = len(self.documents)
            sample_sizes = [s for s in [500, 1000, 2500, 5000] if s <= total_docs]
            if not sample_sizes:
                sample_sizes = [total_docs]

        benchmark_results = []
        builder = IndexBuilder()

        for size in sample_sizes:
            # Subset documents
            subset_docs = self.documents[:size]
            
            # Build slice index for exact evaluation of this subset
            subset_index = builder.build_from_documents(subset_docs)
            search_engine = SearchEngine(subset_index)

            # Benchmark Naive Search
            naive_times = []
            naive_res_count = 0
            for _ in range(runs_per_size):
                res = search_engine.search_naive(query_str=query, limit=10)
                naive_times.append(res["search_time_ms"])
                naive_res_count = res["total_results"]

            avg_naive_ms = sum(naive_times) / len(naive_times)

            # Benchmark Indexed Search
            indexed_times = []
            indexed_res_count = 0
            for _ in range(runs_per_size):
                res = search_engine.search_indexed(query_str=query, limit=10)
                indexed_times.append(res["search_time_ms"])
                indexed_res_count = res["total_results"]

            avg_indexed_ms = sum(indexed_times) / len(indexed_times)

            speedup = calculate_speedup(avg_naive_ms, avg_indexed_ms)

            benchmark_results.append({
                "dataset_size": size,
                "naive_time_ms": round(avg_naive_ms, 3),
                "indexed_time_ms": round(avg_indexed_ms, 3),
                "speedup_factor": speedup,
                "results_count": indexed_res_count
            })

        return {
            "query": query,
            "benchmarks": benchmark_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
