from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., example="కంప్యూటర్ భాష")
    mode: str = Field(default="AND", description="Query mode: AND, OR, SINGLE, PHRASE")
    ranking: str = Field(default="tfidf", description="Ranking method: frequency or tfidf")
    language: Optional[str] = Field(default="all", description="Language filter, e.g., te, hi, all")
    limit: int = Field(default=10, ge=1, le=100)
    page: int = Field(default=1, ge=1)
    use_naive: bool = Field(default=False, description="Use naive baseline search instead of index")


class SearchResultItem(BaseModel):
    document_id: int
    title: str
    language: str
    score: float
    occurrences: int
    matched_terms: List[str]
    snippet: str
    source: Optional[str] = "Wikipedia Sample"


class SearchResponse(BaseModel):
    query: str
    mode: str
    ranking: str
    total_results: int
    search_time_ms: float
    results: List[SearchResultItem]
    page: int
    limit: int
    total_pages: int


class BenchmarkRequest(BaseModel):
    sample_sizes: Optional[List[int]] = Field(default=[500, 1000, 2500, 5000])
    query: Optional[str] = Field(default="కంప్యూటర్")
    runs_per_size: int = Field(default=3, ge=1, le=10)


class BenchmarkItem(BaseModel):
    dataset_size: int
    naive_time_ms: float
    indexed_time_ms: float
    speedup_factor: float
    results_count: int


class BenchmarkResponse(BaseModel):
    query: str
    benchmarks: List[BenchmarkItem]
    timestamp: str


class IndexStatsResponse(BaseModel):
    status: str
    total_documents: int
    total_tokens: int
    unique_terms: int
    avg_tokens_per_doc: float
    max_posting_list_len: int
    index_build_time_sec: float
    index_file_size_mb: float
    languages_supported: Dict[str, int]
    top_20_terms: List[Dict[str, Any]]
