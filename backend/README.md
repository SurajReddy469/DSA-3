# IndicSearch Backend

FastAPI backend service implementing custom Unicode text analytics, posting list data structures, two-pointer set intersection/union, frequency ranking, and TF-IDF scoring for Indian-language Wikipedia documents.

## Directory Layout
- `app/preprocessing/`: Unicode normalization (NFC), cleaner, and tokenization.
- `app/indexing/`: Inverted index, sorted posting lists, two-pointer set operations.
- `app/search/`: Query parser, TF-IDF / Frequency ranking algorithms, context snippet generator.
- `app/evaluation/`: Real-time empirical benchmarking suite.
- `app/api/`: FastAPI REST endpoints (`/api/search`, `/api/stats`, `/api/benchmark`, `/api/health`).
- `scripts/`: CLI pipelines for generating 5,000+ sample documents, preprocessing, index building, and benchmarking.
- `tests/`: Automated unit test suite using `pytest`.

## How to Run

1. Generate sample corpus (5,000+ documents):
```bash
python scripts/generate_sample_dataset.py
```

2. Build inverted index:
```bash
python scripts/build_index.py
```

3. Run API server:
```bash
uvicorn app.main:app --reload --port 8000
```

4. Run tests:
```bash
pytest tests/
```
