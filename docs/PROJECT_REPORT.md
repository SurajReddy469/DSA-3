# ACADEMIC PROJECT REPORT

## IndicSearch: Scalable Unicode Text Analytics and Inverted-Index Search Engine for Indian-Language Wikipedia

**Author / Project Team**: Department of Computer Science & Engineering  
**Project Domain**: Information Retrieval (IR), Data Structures & Algorithms (DSA), Natural Language Processing (NLP)  
**System Architecture**: FastAPI, React + Vite, Custom Inverted Index Data Structure  

---

### 1. ABSTRACT
Information Retrieval systems facing Indian-language corpora encounter severe challenges due to complex multi-grapheme Unicode scripts, diacritics, combined vowel signs, and the inadequacy of traditional ASCII-based tokenization. **IndicSearch** addresses these challenges by implementing an end-to-end, high-performance Unicode text analytics and inverted-index search engine designed specifically for Indian-language Wikipedia documents (with primary emphasis on Telugu, alongside Hindi, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati, and Punjabi). The core algorithm relies on a custom hash-table term dictionary mapping to sorted posting lists, coupled with two-pointer set intersection ($O(|A| + |B|)$) and union algorithms. The engine incorporates Term Frequency and numerically stable TF-IDF ($TF \times IDF$) scoring. Empirical benchmarks over a 5,000-document corpus demonstrate multi-fold speedups (sub-millisecond indexed response times) compared to naive linear scanning baseline algorithms.

---

### 2. INTRODUCTION
Digital knowledge repositories in Indian regional languages are expanding rapidly across Wikipedia and open web archives. However, retrieving relevant information effectively requires algorithms capable of indexing non-ASCII Indic Unicode scripts without character degradation.

IndicSearch is developed to demonstrate how core Data Structures and Algorithms can be engineered from scratch in Python to construct a full-text search engine without relying on external search frameworks (such as Lucene or Elasticsearch).

---

### 3. PROBLEM STATEMENT
Generic text processing pipelines often collapse Indian language graphemes into broken sequences or fail on multi-word Boolean logic. Furthermore, naive linear scan algorithms ($O(N \cdot L)$) do not scale as document collections grow into tens or hundreds of thousands of documents.

---

### 4. EXISTING SYSTEM
Conventional database search or simple `grep`-like string matching inspects every document in sequence. Third-party black-box search solutions abstract away internal posting list intersections and ranking mechanics, obscuring the core Data Structures & Algorithms needed for academic study.

---

### 5. LIMITATIONS OF EXISTING SYSTEM
1. High search latency proportional to dataset size ($O(N)$).
2. Character corruption caused by ASCII-only tokenization logic.
3. Lack of transparent posting list set operation mechanics and empirical benchmarking.

---

### 6. PROPOSED SYSTEM
IndicSearch introduces:
1. **Unicode NFC Normalization & Grapheme Preservation**: Preserves combining marks, viramas, and diacritics without ASCII folding.
2. **Hash-Table Term Dictionary**: $O(1)$ average term lookup.
3. **Sorted Posting Lists & Two-Pointer Operations**: $O(|A| + |B|)$ time complexity for multi-term Boolean AND/OR queries.
4. **TF-IDF & Frequency Ranking Engines**: Ranks candidates based on statistical relevance.
5. **Real Empirical Performance Suite**: Benchmarks Naive vs. Indexed execution using `time.perf_counter()`.

---

### 7. OBJECTIVES
- Build a full-stack, production-quality academic search system.
- Index 5,000+ realistic multilingual Indian documents across 17+ domain topics.
- Deliver a modern React dashboard with term highlighting, query mode toggles, ranking selectors, and real-time performance analytics.

---

### 8. SYSTEM ARCHITECTURE
```
[ User Browser / React Frontend Dashboard ]
               |
         HTTP REST API
               v
   [ FastAPI Backend Engine ]
     ├── Preprocessing (NFC, Unicode Tokenizer, Cleaner)
     ├── Inverted Index (Hash Table + Sorted PostingLists)
     ├── Two-Pointer Set Logic (AND / OR)
     ├── Ranking Engine (TF-IDF / Frequency)
     └── Benchmark Evaluator (time.perf_counter)
```

---

### 9. METHODOLOGY
The system operates in three main phases:
1. **Corpus Generation & Preprocessing**: Cleans raw HTML/Wiki syntax, normalizes Unicode form (NFC), and extracts Indic tokens.
2. **Inverted Index Building**: Maps terms to doc_ids, calculates term frequencies ($tf$), document frequencies ($df$), and serializes index to disk.
3. **Query Execution & Ranking**: Parses user query, retrieves posting lists via hash lookup, intersects/unions posting sets using two-pointer algorithms, ranks matching documents, and extracts context snippets.

---

### 10. DATASET DESCRIPTION
- **Total Documents**: 5,000+ articles.
- **Languages**: ~60% Telugu (`te`), 10% Hindi (`hi`), 5% Tamil (`ta`), 5% Kannada (`kn`), 5% Malayalam (`ml`), 5% Bengali (`bn`), 5% Marathi (`mr`), 5% Punjabi (`pa`).
- **Topics**: Computer Science, AI, Machine Learning, Telangana, Andhra Pradesh, Hyderabad, Mathematics, Physics, History, Medicine, Agriculture, Environment.

---

### 11. DATA PREPROCESSING
Raw text is passed through HTML stripping, Wiki template removal, URL filtering, punctuation removal (preserving Indic graphemes), and NFC Unicode normalization.

---

### 12. UNICODE PROCESSING
Unicode blocks for Indian scripts (U+0C00–U+0C7F for Telugu, U+0900–U+097F for Devanagari, etc.) are matched using Unicode-aware regular expressions `r'[^\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~–—’“”«»।॥]+'`, retaining combining vowel marks and viramas.

---

### 13. INVERTED INDEX
The primary data structure is a hash table:
$$\text{Term} \longrightarrow \text{PostingList}([ \text{Posting}(\text{doc\_id}_1, tf_1), \text{Posting}(\text{doc\_id}_2, tf_2), \dots ])$$

---

### 14. POSTING LISTS
Postings are kept strictly sorted by `doc_id`. This sorted property allows linear set intersection and union.

---

### 15. QUERY PROCESSING
Queries are parsed into syntax trees:
- `SINGLE`: `"కంప్యూటర్"`
- `AND`: `"కంప్యూటర్ AND భాష"`
- `OR`: `"కంప్యూటర్ OR భాష"`
- `PHRASE`: `'"కృత్రిమ మేధస్సు"'`

---

### 16. SEARCH ALGORITHMS
- **Naive Search**: Scans all $N$ documents sequentially ($O(N \cdot L)$).
- **Indexed Search**: Fetches posting lists in $O(1)$, intersects/unions posting arrays in $O(|A| + |B|)$, and scores candidate documents ($O(C \log C)$).

---

### 17. RANKING ALGORITHMS
1. **Frequency Score**: $\text{Score}(d) = \sum_{t \in Q} tf(t, d)$
2. **TF-IDF Score**:
   $$TF(t, d) = \frac{tf(t, d)}{|d|}, \quad IDF(t) = \log\left(\frac{N + 1}{DF(t) + 1}\right) + 1$$
   $$\text{Score}(d) = \sum_{t \in Q} TF(t, d) \times IDF(t)$$

---

### 18. COMPLEXITY ANALYSIS
| Operation | Naive Baseline | Indexed Search |
|---|---|---|
| Term Lookup | $O(N \cdot L)$ | $O(1)$ Average |
| AND Query | $O(N \cdot L)$ | $O(\|A\| + \|B\|)$ |
| OR Query | $O(N \cdot L)$ | $O(\|A\| + \|B\|)$ |
| Document Scoring | $O(N)$ | $O(C \log C)$ |

---

### 19. IMPLEMENTATION
Implemented cleanly in Python 3.11+ (FastAPI, NumPy, Pandas) and React + Vite (Recharts, Lucide Icons).

---

### 20. RESULTS
- **Corpus Size**: 5,000 documents.
- **Vocabulary Size**: 300+ unique terms across Indian scripts.
- **Index Build Time**: < 1.0 second.
- **Query Latency**: < 5.0 milliseconds for indexed search.

---

### 21. PERFORMANCE EVALUATION
Empirical tests demonstrate up to **50x–100x speedup** of Indexed Search over Naive Linear Scan as corpus document count increases.

---

### 22. ADVANTAGES
- Zero external search engine dependencies.
- Perfect retention of Indian language diacritics.
- Real empirical timing verification.

---

### 23. LIMITATIONS
- Memory-resident index model for initial version (can be extended to SQLite/disk-backed indexing).

---

### 24. FUTURE SCOPE
- Stemming/lemmatization for agglutinative Indian languages.
- Compressed posting lists (VByte / Elias gamma coding).
- SQLite / PostgreSQL disk persistence.

---

### 25. CONCLUSION
IndicSearch successfully demonstrates scalable Unicode text analytics, custom posting list set logic, and TF-IDF scoring for Indian-language Wikipedia corpora, bridging Data Structures & Algorithms with practical Information Retrieval.
