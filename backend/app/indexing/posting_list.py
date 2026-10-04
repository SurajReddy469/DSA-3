from typing import List, Optional, Dict, Any


class Posting:
    """
    Represents a single posting entry in a term's posting list.
    Contains document identifier, term frequency in document, and positional occurrences.
    """
    __slots__ = ('doc_id', 'tf', 'positions')

    def __init__(self, doc_id: int, tf: int = 1, positions: Optional[List[int]] = None):
        self.doc_id: int = doc_id
        self.tf: int = tf
        self.positions: List[int] = positions if positions is not None else []

    def add_occurrence(self, position: int):
        self.tf += 1
        self.positions.append(position)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "frequency": self.tf,
            "positions": self.positions
        }

    def __repr__(self):
        return f"Posting(doc_id={self.doc_id}, tf={self.tf})"


class PostingList:
    """
    Sorted list of postings ordered by doc_id.
    Maintains document frequency (df) and allows rapid set operations.
    """

    def __init__(self):
        self.postings: List[Posting] = []

    @property
    def df(self) -> int:
        """Document Frequency (number of documents containing the term)."""
        return len(self.postings)

    def add_posting(self, doc_id: int, tf: int = 1, position: Optional[int] = None):
        """
        Adds or updates a posting. Assumes additions happen in monotonically increasing
        doc_id order during index building.
        """
        if self.postings and self.postings[-1].doc_id == doc_id:
            self.postings[-1].tf += tf
            if position is not None:
                self.postings[-1].positions.append(position)
        else:
            p = Posting(doc_id=doc_id, tf=tf)
            if position is not None:
                p.positions.append(position)
            self.postings.append(p)

    def get_postings(self) -> List[Posting]:
        return self.postings

    def __len__(self) -> int:
        return len(self.postings)

    def __iter__(self):
        return iter(self.postings)


def intersect_postings(p1: PostingList, p2: PostingList) -> PostingList:
    """
    Optimized Two-Pointer Posting List Intersection (AND query).

    Algorithm:
    - Maintain pointer i for p1 and pointer j for p2.
    - Advance the pointer pointing to the smaller document ID.
    - If doc_ids match, append to result and advance both pointers.

    Complexity Analysis:
    - Time Complexity: O(|A| + |B|) where |A| and |B| are the posting list lengths.
    - Space Complexity: O(min(|A|, |B|)) for the output posting list.
    """
    result = PostingList()
    if not p1 or not p2:
        return result

    postings1 = p1.postings
    postings2 = p2.postings

    i, j = 0, 0
    len1, len2 = len(postings1), len(postings2)

    while i < len1 and j < len2:
        doc1 = postings1[i].doc_id
        doc2 = postings2[j].doc_id

        if doc1 == doc2:
            # Combine term frequencies for scoring
            combined_tf = postings1[i].tf + postings2[j].tf
            combined_pos = postings1[i].positions + postings2[j].positions
            res_posting = Posting(doc_id=doc1, tf=combined_tf, positions=combined_pos)
            result.postings.append(res_posting)
            i += 1
            j += 1
        elif doc1 < doc2:
            i += 1
        else:
            j += 1

    return result


def union_postings(p1: PostingList, p2: PostingList) -> PostingList:
    """
    Optimized Two-Pointer Posting List Union (OR query).

    Algorithm:
    - Maintain pointer i for p1 and pointer j for p2.
    - Append the posting with the smaller document ID.
    - If doc_ids match, append a merged posting and advance both.

    Complexity Analysis:
    - Time Complexity: O(|A| + |B|) where |A| and |B| are posting list lengths.
    - Space Complexity: O(|A| + |B|) for output posting list.
    """
    result = PostingList()
    postings1 = p1.postings if p1 else []
    postings2 = p2.postings if p2 else []

    i, j = 0, 0
    len1, len2 = len(postings1), len(postings2)

    while i < len1 and j < len2:
        doc1 = postings1[i].doc_id
        doc2 = postings2[j].doc_id

        if doc1 == doc2:
            combined_tf = postings1[i].tf + postings2[j].tf
            combined_pos = postings1[i].positions + postings2[j].positions
            res_posting = Posting(doc_id=doc1, tf=combined_tf, positions=combined_pos)
            result.postings.append(res_posting)
            i += 1
            j += 1
        elif doc1 < doc2:
            result.postings.append(Posting(doc1, postings1[i].tf, list(postings1[i].positions)))
            i += 1
        else:
            result.postings.append(Posting(doc2, postings2[j].tf, list(postings2[j].positions)))
            j += 1

    while i < len1:
        result.postings.append(Posting(postings1[i].doc_id, postings1[i].tf, list(postings1[i].positions)))
        i += 1

    while j < len2:
        result.postings.append(Posting(postings2[j].doc_id, postings2[j].tf, list(postings2[j].positions)))
        j += 1

    return result
