# IndicSearch
### Scalable Unicode Text Analytics and Inverted-Index Search Engine for Indian-Language Wikipedia

**IndicSearch** is a full-stack, production-quality academic search engine and text analytics platform engineered from scratch to provide fast keyword search over Indian-language Wikipedia corpora (with primary focus on Telugu, plus support for Hindi, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati, and Punjabi).

It implements core Data Structures & Algorithms (DSA)—including hash-table term dictionaries, sorted posting lists, two-pointer set intersection/union ($O(|A| + |B|)$), frequency ranking, and TF-IDF scoring—without delegating core search tasks to third-party search libraries.

---

## 🌟 Key Features
- **Unicode Support & Grapheme Preservation**: Full NFC Unicode normalization preserving combining vowel signs, diacritics, and virama without ASCII folding.
- **Custom Inverted Index**: Hash table dictionary mapping terms to sorted posting lists for $O(1)$ average term lookups.
- **Two-Pointer Set Operations**: High-performance $O(|A| + |B|)$ posting list intersection and union algorithms.
- **Multiple Ranking Models**: Switch dynamically between Term Frequency and numerically stable TF-IDF ($TF \times IDF$).
- **Multi-Keyword & Boolean Search**: Supports Single term, `AND`, `OR`, and phrase queries.
- **Real Empirical Benchmarking**: Evaluates high-resolution search execution time (`time.perf_counter()`) comparing Naive linear scan vs. Inverted Index search.
- **5,000+ Multilingual Corpus Generator**: Automatic dataset generator producing realistic Indian-language articles across 17+ domain topics.
- **Interactive Dashboard**: Modern React + Vite frontend with term highlighting, language filters, page limits, and Recharts performance analytics.

---

## 📁 Repository Structure
```
IndicSearch/
│
├── backend/
│   ├── app/
│   │   ├── preprocessing/     # Unicode NFC, cleaner, tokenizer
│   │   ├── indexing/          # InvertedIndex, PostingList, two-pointer set logic
│   │   ├── search/            # Query parser, TF-IDF ranker, snippet generator
│   │   ├── evaluation/        # Empirical benchmarking suite
│   │   └── api/               # FastAPI REST endpoints
│   ├── data/                  # Corpus JSON & pickled inverted index
│   ├── scripts/               # CLI dataset generator, index builder, benchmark script
│   ├── tests/                 # Automated pytest suite
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/        # SearchBar, SearchResults, RankingSelector, PerformanceChart
│   │   ├── pages/             # Home, Analytics, About
│   │   ├── services/          # Axios API service
│   │   └── App.jsx
│   ├── package.json
│   └── README.md
│
├── docs/
│   ├── PROJECT_REPORT.md      # Comprehensive 25-section academic report
│   ├── ALGORITHM_DOCUMENTATION.md # Mathematical & DSA documentation + pseudocode
│   ├── API_DOCUMENTATION.md   # OpenAPI REST endpoint specs
│   └── SETUP_GUIDE.md         # Detailed setup instructions
│
├── README.md
└── .gitignore
```

---

## 🚀 Quick Execution Instructions

### 1. Backend (FastAPI API Engine)
```bash
cd backend
pip install -r requirements.txt
python scripts/generate_sample_dataset.py
python scripts/build_index.py
python -m pytest tests/
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (React Dashboard)
```bash
cd frontend
npm install
npm run dev
```

Open browser at `http://localhost:5173`.

---

## 🧪 Demonstration Queries
- Single Keyword: `కంప్యూటర్`
- Phrase Match: `"కృత్రిమ మేధస్సు"`
- Boolean AND: `కంప్యూటర్ AND భాష`
- Boolean OR: `కంప్యూటర్ OR భాష`
- Regional Topic: `తెలంగాణ` or `హైదరాబాద్`
- Science & Math: `గణితం`
