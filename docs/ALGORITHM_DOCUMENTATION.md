# ALGORITHM DOCUMENTATION — IndicSearch

This document explains the core Data Structures and Algorithms (DSA) implemented in **IndicSearch**.

---

## 1. HASH-TABLE TERM DICTIONARY

The primary index dictionary uses Python's underlying hash table (`dict[str, PostingList]`) to map terms to posting list objects.

### Complexity
- **Average Time Complexity**: $O(1)$ lookup and insertion.
- **Worst Case Time Complexity**: $O(k)$ where $k$ is key length in characters.

---

## 2. POSTING LIST & POSTING STRUCTURE

A `Posting` represents the occurrence of a term in a document:

```python
class Posting:
    doc_id: int
    tf: int  # Term Frequency in this document
    positions: List[int]
```

A `PostingList` maintains an array of `Posting` objects kept strictly sorted by `doc_id`.

---

## 3. TWO-POINTER POSTING LIST INTERSECTION (AND QUERY)

When evaluating a multi-term Boolean AND query $T_1 \text{ AND } T_2$, the system intersects posting list $P_1$ and posting list $P_2$.

### Pseudocode
```text
ALGORITHM IntersectPostings(P1, P2):
    Input: Sorted PostingLists P1 and P2
    Output: Result PostingList containing matching document postings

    result = new PostingList()
    i = 0, j = 0

    WHILE i < length(P1) AND j < length(P2) DO:
        doc1 = P1[i].doc_id
        doc2 = P2[j].doc_id

        IF doc1 == doc2 THEN:
            combined_tf = P1[i].tf + P2[j].tf
            result.append(Posting(doc1, combined_tf))
            i = i + 1
            j = j + 1
        ELSE IF doc1 < doc2 THEN:
            i = i + 1
        ELSE:
            j = j + 1
        END IF
    END WHILE

    RETURN result
```

### Complexity Analysis
- **Time Complexity**: $O(|P_1| + |P_2|)$ linear scan over candidate arrays.
- **Space Complexity**: $O(\min(|P_1|, |P_2|))$ for output postings.

---

## 4. TWO-POINTER POSTING LIST UNION (OR QUERY)

Evaluates Boolean OR query by merging two sorted posting lists in linear time.

### Pseudocode
```text
ALGORITHM UnionPostings(P1, P2):
    Input: Sorted PostingLists P1 and P2
    Output: Result PostingList containing union of postings

    result = new PostingList()
    i = 0, j = 0

    WHILE i < length(P1) AND j < length(P2) DO:
        doc1 = P1[i].doc_id
        doc2 = P2[j].doc_id

        IF doc1 == doc2 THEN:
            result.append(Posting(doc1, P1[i].tf + P2[j].tf))
            i = i + 1; j = j + 1
        ELSE IF doc1 < doc2 THEN:
            result.append(P1[i]); i = i + 1
        ELSE:
            result.append(P2[j]); j = j + 1
        END IF
    END WHILE

    WHILE i < length(P1) DO result.append(P1[i]); i = i + 1
    WHILE j < length(P2) DO result.append(P2[j]); j = j + 1

    RETURN result
```

### Complexity Analysis
- **Time Complexity**: $O(|P_1| + |P_2|)$
- **Space Complexity**: $O(|P_1| + |P_2|)$

---

## 5. TF-IDF RANKING FORMULA

$$\text{TF}(t, d) = \frac{\text{count}(t, d)}{\text{length}(d)}$$

$$\text{IDF}(t) = \log\left(\frac{N + 1}{\text{DF}(t) + 1}\right) + 1$$

$$\text{Score}(d) = \sum_{t \in Q} \text{TF}(t, d) \times \text{IDF}(t)$$

Where $N$ is total documents in corpus, and $\text{DF}(t)$ is document frequency of term $t$.
