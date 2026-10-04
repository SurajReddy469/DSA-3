# SETUP GUIDE — IndicSearch

Follow these step-by-step instructions to set up, build, test, and run IndicSearch on Windows/macOS/Linux.

---

## PREREQUISITES
- Python 3.11+
- Node.js 18+ and npm

---

## STEP 1: BACKEND SETUP

1. Navigate to the backend folder:
```bash
cd backend
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv .venv
```
- **Windows**: `.venv\Scripts\activate`
- **Linux/macOS**: `source .venv/bin/activate`

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

4. Generate 5,000-document sample dataset:
```bash
python scripts/generate_sample_dataset.py
```

5. Build the Inverted Index:
```bash
python scripts/build_index.py
```

6. Run unit tests to verify system health:
```bash
python -m pytest tests/
```

7. Start the FastAPI API server:
```bash
uvicorn app.main:app --reload --port 8000
```
Backend API interactive documentation is available at `http://localhost:8000/docs`.

---

## STEP 2: FRONTEND SETUP

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the Vite React development server:
```bash
npm run dev
```

4. Open your browser at:
`http://localhost:5173`
