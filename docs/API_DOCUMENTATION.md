# API DOCUMENTATION — IndicSearch Engine REST Endpoints

Base URL: `http://localhost:8000/api`

---

## 1. GET /api/health
Returns service health status and index initialization status.

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "service": "IndicSearch API",
  "index_loaded": true
}
```

---

## 2. GET /api/stats
Returns corpus and inverted index statistics.

**Response (200 OK)**:
```json
{
  "status": "ready",
  "total_documents": 5000,
  "total_tokens": 184891,
  "unique_terms": 307,
  "avg_tokens_per_doc": 36.98,
  "max_posting_list_len": 3003,
  "index_build_time_sec": 0.546,
  "index_file_size_mb": 0.65,
  "languages_supported": {
    "te": 3000,
    "hi": 500,
    "ta": 250,
    "kn": 250,
    "ml": 250,
    "bn": 250,
    "mr": 250,
    "pa": 250
  },
  "top_20_terms": [...]
}
```

---

## 3. POST /api/search
Executes keyword search query.

**Request Payload**:
```json
{
  "query": "కంప్యూటర్ భాష",
  "mode": "AND",
  "ranking": "tfidf",
  "language": "all",
  "limit": 10,
  "page": 1,
  "use_naive": false
}
```

**Response (200 OK)**:
```json
{
  "query": "కంప్యూటర్ భాష",
  "mode": "AND",
  "ranking": "tfidf",
  "total_results": 12,
  "search_time_ms": 1.45,
  "results": [
    {
      "document_id": 21,
      "title": "కంప్యూటర్ భాష",
      "language": "te",
      "score": 12.84,
      "occurrences": 8,
      "matched_terms": ["కంప్యూటర్", "భాష"],
      "snippet": "కంప్యూటర్ <mark>భాష</mark> మరియు ప్రోగ్రామింగ్..."
    }
  ],
  "page": 1,
  "limit": 10,
  "total_pages": 2
}
```

---

## 4. POST /api/benchmark
Runs empirical timing comparison between Naive Search and Inverted Index Search.

**Request Payload**:
```json
{
  "query": "కంప్యూటర్",
  "sample_sizes": [500, 1000, 2500, 5000],
  "runs_per_size": 3
}
```

**Response (200 OK)**:
```json
{
  "query": "కంప్యూటర్",
  "benchmarks": [
    {
      "dataset_size": 500,
      "naive_time_ms": 8.12,
      "indexed_time_ms": 0.45,
      "speedup_factor": 18.04,
      "results_count": 300
    },
    {
      "dataset_size": 5000,
      "naive_time_ms": 78.45,
      "indexed_time_ms": 0.85,
      "speedup_factor": 92.29,
      "results_count": 3000
    }
  ],
  "timestamp": "2026-10-04 21:40:00"
}
```
