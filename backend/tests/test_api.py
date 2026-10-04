import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import initialize_index, index_instance
from app.indexing.index_builder import IndexBuilder


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_index():
    docs = [
        {"document_id": 1, "title": "కంప్యూటర్", "language": "te", "text": "కంప్యూటర్ మరియు ఆధునిక పరిజ్ఞానం", "source": "Test"},
        {"document_id": 2, "title": "కృత్రిమ మేధస్సు", "language": "te", "text": "కృత్రిమ మేధస్సు మరియు డేటా విశ్లేషణ", "source": "Test"}
    ]
    builder = IndexBuilder()
    idx = builder.build_from_documents(docs)
    
    import app.api.routes as routes
    routes.index_instance = idx
    routes.search_engine_instance = routes.SearchEngine(idx)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "healthy"
    assert json_resp["index_loaded"] is True


def test_stats_endpoint():
    response = client.get("/api/stats")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["total_documents"] == 2
    assert json_resp["unique_terms"] > 0


def test_search_endpoint():
    payload = {
        "query": "కంప్యూటర్",
        "mode": "AND",
        "ranking": "tfidf",
        "limit": 10,
        "page": 1
    }
    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["total_results"] == 1
    assert len(json_resp["results"]) == 1
    assert json_resp["results"][0]["document_id"] == 1
