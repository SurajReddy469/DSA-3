import pytest
from app.indexing.posting_list import PostingList, intersect_postings, union_postings
from app.indexing.inverted_index import InvertedIndex
from app.indexing.index_builder import IndexBuilder


def test_posting_list_operations():
    p1 = PostingList()
    p1.add_posting(1, tf=3)
    p1.add_posting(5, tf=1)
    p1.add_posting(9, tf=2)
    p1.add_posting(15, tf=4)

    p2 = PostingList()
    p2.add_posting(2, tf=1)
    p2.add_posting(5, tf=2)
    p2.add_posting(9, tf=1)
    p2.add_posting(20, tf=3)

    # Test two-pointer intersection: expected doc_ids [5, 9]
    intersect_res = intersect_postings(p1, p2)
    matched_doc_ids = [p.doc_id for p in intersect_res.get_postings()]
    assert matched_doc_ids == [5, 9]

    # Test two-pointer union: expected doc_ids [1, 2, 5, 9, 15, 20]
    union_res = union_postings(p1, p2)
    union_doc_ids = [p.doc_id for p in union_res.get_postings()]
    assert union_doc_ids == [1, 2, 5, 9, 15, 20]


def test_inverted_index_building():
    docs = [
        {"document_id": 1, "title": "కంప్యూటర్", "language": "te", "text": "కంప్యూటర్ ఒక పరికరం", "source": "Test"},
        {"document_id": 2, "title": "భాష", "language": "te", "text": "కంప్యూటర్ భాష మరియు ప్రోగ్రామింగ్", "source": "Test"}
    ]

    builder = IndexBuilder()
    index = builder.build_from_documents(docs)

    assert index.total_documents == 2
    assert index.get_doc_frequency("కంప్యూటర్") == 2
    assert index.get_doc_frequency("పరికరం") == 1

    postings = index.get_postings("కంప్యూటర్").get_postings()
    assert [p.doc_id for p in postings] == [1, 2]
