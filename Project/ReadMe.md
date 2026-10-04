# IndicSearch 🔎

### Data Structures and Algorithms Based Search Engine

IndicSearch is a search engine project developed as a **Data Structures and Algorithms (DSA)** project. The system provides a web-based interface for searching and retrieving information using efficient data structures and search algorithms.

The project combines a **FastAPI backend** with a modern **Vite-based frontend** to provide an interactive search experience.

---

## 🚀 Features

- 🔍 Fast and efficient search
- 🌐 Web-based user interface
- ⚡ FastAPI backend
- 🖥️ Modern frontend using Vite
- 🧠 Data Structures and Algorithms based search implementation
- 📊 Search and retrieval functionality
- 🧪 Automated backend testing
- 📚 Interactive API documentation using Swagger
- 🔄 REST API communication between frontend and backend

---

## 🏗️ Project Architecture

```text
IndicSearch/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── ...
│   ├── tests/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- Pytest

### Frontend

- JavaScript
- Vite
- HTML
- CSS

### Core DSA Concepts

- Searching
- Data organization
- Efficient data retrieval
- Algorithmic processing
- Time and space complexity analysis

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/IndicSearch.git
```

Move into the project directory:

```bash
cd IndicSearch
```

---

# 🔹 Backend Setup

Open a terminal and navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Backend

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

### API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 🔹 Frontend Setup

Open a **new terminal** while keeping the backend running.

Navigate to the frontend:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Open the URL in your browser.

---

# 🧪 Testing

The backend contains automated tests.

Navigate to the backend:

```bash
cd backend
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the tests:

```bash
pytest
```

The current project test suite passes:

```text
10 passed
```

---

# 📡 API

The backend is built using FastAPI.

### Root Endpoint

```http
GET /
```

Returns information about the IndicSearch API.

### Health Check

```http
GET /api/health
```

Used to verify that the backend is running correctly.

### API Documentation

```text
GET /docs
```

Provides interactive Swagger documentation for the available API endpoints.

---

# 🧠 DSA Concepts

The main objective of IndicSearch is to demonstrate how **Data Structures and Algorithms** can be applied to build an efficient search system.

The project focuses on:

- Efficient data storage
- Searching techniques
- Data indexing
- Information retrieval
- Algorithmic optimization
- Complexity analysis

The DSA components form the core logic behind the search functionality, while the web application provides an interface for users to interact with the system.

---

# 📈 Project Workflow

```text
             User
               │
               ▼
        ┌───────────────┐
        │   Frontend    │
        │ Vite Web App  │
        └───────┬───────┘
                │
                │ HTTP Requests
                ▼
        ┌───────────────┐
        │    FastAPI    │
        │    Backend    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ DSA Search    │
        │ Algorithms    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Search Results│
        └───────────────┘
```

---

# 💻 Running the Complete Project

You need **two terminals**.

### Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# 📋 Requirements

Make sure you have the following installed:

- Python 3.10+
- pip
- Node.js
- npm
- Git

---

# 👨‍💻 Project

**Project Name:** IndicSearch

**Project Type:** Data Structures and Algorithms Project

**Backend:** FastAPI + Python

**Frontend:** Vite + JavaScript

---

# 📜 License

This project was developed for educational and academic purposes.

---

## ⭐ Acknowledgement

This project was developed as part of a **Data Structures and Algorithms (DSA)** academic project to demonstrate the practical application of data structures, searching algorithms, backend APIs, and web technologies.
