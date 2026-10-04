import os
from pathlib import Path

# Base backend paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INDEX_DATA_DIR = DATA_DIR / "index"

# Create directories if they do not exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_CORPUS_PATH = RAW_DATA_DIR / "corpus.json"
PROCESSED_CORPUS_PATH = PROCESSED_DATA_DIR / "processed_corpus.json"
INDEX_FILE_PATH = INDEX_DATA_DIR / "inverted_index.pkl"
INDEX_METADATA_PATH = INDEX_DATA_DIR / "index_metadata.json"

# Search Defaults
DEFAULT_SNIPPET_LENGTH = 160
DEFAULT_MAX_RESULTS = 50

# Supported Languages
SUPPORTED_LANGUAGES = {
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "en": "English", # Supported for bilingual queries
    "all": "All Languages"
}
