import json
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from app.models import (
    SearchRequest, SearchResponse, BenchmarkRequest, BenchmarkResponse, IndexStatsResponse
)
from app.indexing.inverted_index import InvertedIndex
from app.indexing.index_builder import build_and_save_index
from app.search.search_engine import SearchEngine
from app.evaluation.benchmark import PerformanceBenchmark
from app.config import RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH

router = APIRouter(prefix="/api")

# Global in-memory index & engine singleton instance
index_instance: InvertedIndex = None
search_engine_instance: SearchEngine = None


def get_search_engine() -> SearchEngine:
    global search_engine_instance
    if search_engine_instance is None:
        raise HTTPException(status_code=503, detail="Search engine index is not initialized or ready.")
    return search_engine_instance


def initialize_index():
    """Pre-loads or builds inverted index on application startup."""
    global index_instance, search_engine_instance
    if INDEX_FILE_PATH.exists():
        try:
            index_instance = InvertedIndex.load_index(INDEX_FILE_PATH)
            search_engine_instance = SearchEngine(index_instance)
            return
        except Exception:
            pass

    # Build fallback index if file does not exist
    if RAW_CORPUS_PATH.exists():
        index_instance = build_and_save_index(RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH)
        search_engine_instance = SearchEngine(index_instance)


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "IndicSearch API",
        "index_loaded": index_instance is not None
    }


@router.get("/index/status")
def index_status():
    """Returns inverted index operational status."""
    if index_instance is None:
        return {"ready": False, "message": "Index not loaded"}
    return {
        "ready": True,
        "total_documents": index_instance.total_documents,
        "unique_terms": len(index_instance.term_dict),
        "build_time_sec": index_instance.build_time_sec
    }


@router.get("/stats", response_model=IndexStatsResponse)
def get_stats():
    """Returns detailed statistics about the corpus and inverted index."""
    if index_instance is None:
        raise HTTPException(status_code=503, detail="Index is not loaded")
    stats = index_instance.get_stats()
    stats["status"] = "ready"
    stats["index_file_size_mb"] = (
        round(INDEX_FILE_PATH.stat().st_size / (1024.0 * 1024.0), 3)
        if INDEX_FILE_PATH.exists() else 0.0
    )
    return stats


@router.post("/search", response_model=SearchResponse)
def search_corpus(req: SearchRequest, engine: SearchEngine = Depends(get_search_engine)):
    """
    Executes keyword search over Indian-language corpus.
    Supports single term, multi-term AND, OR, Frequency ranking, TF-IDF, and language filter.
    """
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Search query string cannot be empty.")

    if req.use_naive:
        res = engine.search_naive(
            query_str=req.query,
            mode=req.mode,
            ranking=req.ranking,
            language=req.language,
            limit=req.limit,
            page=req.page
        )
    else:
        res = engine.search_indexed(
            query_str=req.query,
            mode=req.mode,
            ranking=req.ranking,
            language=req.language,
            limit=req.limit,
            page=req.page
        )

    return res


@router.post("/benchmark", response_model=BenchmarkResponse)
def run_benchmark(req: BenchmarkRequest):
    """
    Runs real-time empirical performance comparison between Naive Search and Indexed Search.
    """
    if index_instance is None:
        raise HTTPException(status_code=503, detail="Index is not loaded")

    raw_docs = []
    if RAW_CORPUS_PATH.exists():
        with open(RAW_CORPUS_PATH, 'r', encoding='utf-8') as f:
            raw_docs = json.load(f)

    if not raw_docs:
        raise HTTPException(status_code=400, detail="Corpus data unavailable for benchmark")

    benchmarker = PerformanceBenchmark(full_index=index_instance, documents=raw_docs)
    res = benchmarker.run_benchmark(
        query=req.query,
        sample_sizes=req.sample_sizes,
        runs_per_size=req.runs_per_size
    )
    return res


@router.post("/index/build")
def trigger_index_rebuild():
    """Rebuilds inverted index from raw dataset."""
    global index_instance, search_engine_instance
    if not RAW_CORPUS_PATH.exists():
        raise HTTPException(status_code=400, detail="Raw corpus file not found. Generate sample dataset first.")

    index_instance = build_and_save_index(RAW_CORPUS_PATH, INDEX_FILE_PATH, INDEX_METADATA_PATH)
    search_engine_instance = SearchEngine(index_instance)
    
    return {
        "status": "success",
        "message": "Index rebuilt successfully",
        "total_documents": index_instance.total_documents,
        "unique_terms": len(index_instance.term_dict),
        "build_time_sec": index_instance.build_time_sec
    }


@router.get("/documents/{document_id}")
def get_document_details(document_id: int = Path(..., ge=1)):
    """Fetches details for a specific document ID."""
    if index_instance is None:
        raise HTTPException(status_code=503, detail="Index is not loaded")
    
    meta = index_instance.doc_metadata.get(document_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found.")

    return meta
