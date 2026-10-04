import pytest
from app.indexing.index_builder import IndexBuilder
from app.search.query_parser import QueryParser
from app.search.search_engine import SearchEngine


def test_query_parser():
    parser = QueryParser()
    
    q1 = parser.parse("కంప్యూటర్")
    assert q1.operator == "SINGLE"
    assert q1.terms == ["కంప్యూటర్"]

    q2 = parser.parse("కంప్యూటర్ AND భాష")
    assert q2.operator == "AND"
    assert "కంప్యూటర్" in q2.terms
    assert "భాష" in q2.terms

    q3 = parser.parse("కంప్యూటర్ OR భాష")
    assert q3.operator == "OR"
    assert "కంప్యూటర్" in q3.terms
    assert "భాష" in q3.terms


def test_search_engine_ranking():
    docs = [
        {"document_id": 1, "title": "కంప్యూటర్ సైన్స్", "language": "te", "text": "కంప్యూటర్ కంప్యూటర్ కంప్యూటర్ పరిజ్ఞానం", "source": "Test"},
        {"document_id": 2, "title": "కృత్రిమ మేధస్సు", "language": "te", "text": "కంప్యూటర్ మరియు కృత్రిమ మేధస్సు", "source": "Test"},
        {"document_id": 3, "title": "గణితం", "language": "te", "text": "గణిత శాస్త్ర వివరణ", "source": "Test"}
    ]

    builder = IndexBuilder()
    index = builder.build_from_documents(docs)
    engine = SearchEngine(index)

    # Test AND search
    res_and = engine.search_indexed("కంప్యూటర్ AND కృత్రిమ", mode="AND", ranking="tfidf")
    assert res_and["total_results"] == 1
    assert res_and["results"][0]["document_id"] == 2

    # Test OR search
    res_or = engine.search_indexed("కంప్యూటర్ OR మేధస్సు", mode="OR", ranking="frequency")
    assert res_or["total_results"] == 2

    # Frequency ranking order check: Doc 1 has higher frequency of 'కంప్యూటర్'
    res_freq = engine.search_indexed("కంప్యూటర్", mode="SINGLE", ranking="frequency")
    assert res_freq["results"][0]["document_id"] == 1
