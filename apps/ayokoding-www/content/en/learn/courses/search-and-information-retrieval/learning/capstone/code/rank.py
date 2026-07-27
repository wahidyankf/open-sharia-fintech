# pyright: strict
"""Capstone Step 2: rank.py -- adds TF-IDF then BM25 top-k scoring on top of index.py's
typed InvertedIndex (co-14, co-16, co-20).

Verify: the ranked order matches a hand-computed BM25 score on a 3-document fixture.
"""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import heapq  # => stdlib binary heap -- backs the size-k top-k selection
import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing

from index import (
    CORPUS,
    InvertedIndex,
    analyze,
    build_index,
)  # => from index: CORPUS, InvertedIndex, analyze, build_index


def tfidf_score(
    index: InvertedIndex, query_terms: list[str], doc_id: int
) -> (
    float
):  # => co-14: sum of tf * log(N / df) over every query term the document contains
    """co-14: sum of tf * log(N / df) over every query term the document contains."""
    n_docs: int = len(index.doc_lengths)  # => co-14: N, the corpus size
    total: float = 0.0  # => total = 0.0
    for term in query_terms:  # => iterates one item at a time
        doc_tfs: dict[int, int] = index.postings.get(
            term, {}
        )  # => doc tfs = index.postings.get(term, {})
        if doc_id in doc_tfs:  # => true when doc_id in doc_tfs
            df: int = len(doc_tfs)  # => co-13: how many documents contain this term
            total += doc_tfs[doc_id] * math.log(
                n_docs / df
            )  # => co-14: tf * idf, summed
    return total  # => returns total


def bm25_score(
    index: InvertedIndex,
    query_terms: list[str],
    doc_id: int,
    avgdl: float,
    k1: float = 1.2,
    b: float = 0.75,
) -> float:  # => co-16: BM25's own RSJ idf, saturating tf, and length normalization -- summed per term
    """co-16: BM25's own RSJ idf, saturating tf, and length normalization -- summed per term."""
    n_docs: int = len(index.doc_lengths)  # => this fixture's own size
    dl: float = float(index.doc_lengths[doc_id])  # => co-18: this document's own length
    total: float = 0.0  # => total = 0.0
    for term in query_terms:  # => iterates one item at a time
        doc_tfs: dict[int, int] = index.postings.get(
            term, {}
        )  # => doc tfs = index.postings.get(term, {})
        if doc_id in doc_tfs:  # => true when doc_id in doc_tfs
            tf: int = doc_tfs[doc_id]  # => tf = doc_tfs[doc_id]
            df: int = len(doc_tfs)  # => this fixture's own size
            idf: float = math.log(
                (n_docs - df + 0.5) / (df + 0.5)
            )  # => co-16: RSJ idf, not plain log(N/df)
            B: float = (1 - b) + b * (dl / avgdl)  # => co-18: length normalization
            total += (
                idf * (tf * (k1 + 1)) / (tf + k1 * B)
            )  # => co-17: the saturating term score
    return total  # => returns total


def rank_bm25_topk(
    index: InvertedIndex, query: str, k: int
) -> list[
    tuple[int, float]
]:  # => co-20: BM25-score every candidate document, return the top k via a size-k heap
    """co-20: BM25-score every candidate document, return the top k via a size-k heap."""
    query_terms: list[str] = analyze(
        query
    )  # => co-25: the SAME analyzer used at index time
    n_docs: int = len(index.doc_lengths)  # => this fixture's own size
    if n_docs == 0:  # => true when n_docs == 0
        return []  # => returns []
    avgdl: float = (
        sum(index.doc_lengths.values()) / n_docs
    )  # => co-18: this index's own average document length
    candidates: set[int] = (
        set()
    )  # => co-01: only documents matching AT LEAST ONE query term are scored
    for term in query_terms:  # => iterates one item at a time
        candidates |= set(
            index.postings.get(term, {}).keys()
        )  # => part of this step's computation, continued from the line above

    scored: list[tuple[float, int]] = [
        (bm25_score(index, query_terms, doc_id, avgdl), doc_id) for doc_id in candidates
    ]  # => scored = [(bm25_score(index, query_terms, doc_id, avgdl)...
    return [
        (doc_id, s) for s, doc_id in heapq.nlargest(k, scored)
    ]  # => co-20: top-k via heap, not a full sort


def main() -> None:  # => defines main
    index: InvertedIndex = build_index(
        CORPUS
    )  # => co-01: the full capstone index, from index.py
    query: str = "search index"  # => a 2-term query matching several documents to varying degrees

    top3: list[tuple[int, float]] = rank_bm25_topk(
        index, query, k=3
    )  # => co-16, co-20: BM25 top-3
    print(f"BM25 top-3 for {query!r}: {top3}")  # => shows BM25 top-3 for

    # A tiny, SEPARATE 3-document fixture, hand-computed independently of rank_bm25_topk.
    # Both query terms appear ONLY in doc 0 (df=1 each) -- chosen deliberately so their RSJ idf
    # values are equal and positive, avoiding the reciprocal-idf coincidence a df=1-vs-df=2 pair
    # would trigger on such a tiny N=3 corpus.
    fixture: dict[int, str] = {
        0: "search index engine",
        1: "results page display",
        2: "cooking recipe book",
    }  # => fixture = {0: "search index engine", 1: "results page dis...
    fixture_index: InvertedIndex = build_index(
        fixture
    )  # => co-01: a fresh, tiny index just for this hand check
    fixture_top: list[tuple[int, float]] = rank_bm25_topk(
        fixture_index, "search index", k=3
    )  # => fixture top = rank_bm25_topk(fixture_index, "search index", k=3)
    print(f"fixture BM25 ranking: {fixture_top}")  # => shows fixture BM25 ranking

    n_docs, avgdl = (
        3,
        sum(fixture_index.doc_lengths.values()) / 3,
    )  # => the fixture's own N and avgdl
    df_search, df_index = (
        1,
        1,
    )  # => BOTH terms appear only in doc 0 -- equal, positive idf
    hand_idf_search: float = math.log(
        (n_docs - df_search + 0.5) / (df_search + 0.5)
    )  # => hand idf search = math.log((n_docs - df_search + 0.5) / (df_searc...
    hand_idf_index: float = math.log(
        (n_docs - df_index + 0.5) / (df_index + 0.5)
    )  # => hand idf index = math.log((n_docs - df_index + 0.5) / (df_index ...
    hand_B0: float = (1 - 0.75) + 0.75 * (
        fixture_index.doc_lengths[0] / avgdl
    )  # => hand B0 = (1 - 0.75) + 0.75 * (fixture_index.doc_lengths[...
    hand_score_doc0: float = (  # => hand score doc0 = (
        hand_idf_search * (1 * 2.2) / (1 + 1.2 * hand_B0)
        + hand_idf_index
        * (1 * 2.2)
        / (
            1 + 1.2 * hand_B0
        )  # => part of this step's computation, continued from the line above
    )  # => opens/closes this multi-line literal
    print(
        f"hand-computed BM25 score for fixture doc 0: {hand_score_doc0:.6f}"
    )  # => shows hand-computed BM25 score for fixture doc 0

    assert fixture_top[0][0] == 0, (
        "fixture doc 0 (matches BOTH query terms) must rank first"
    )  # => fixture doc 0 (matches BOTH query terms) must rank first
    assert math.isclose(fixture_top[0][1], hand_score_doc0, rel_tol=1e-9), (
        "rank_bm25_topk's top score must equal the hand computation"
    )  # => rank_bm25_topk's top score must equal the hand computation
    print(
        f"MATCH: rank_bm25_topk's top score {fixture_top[0][1]:.6f} equals the hand-computed BM25 score {hand_score_doc0:.6f}"
    )  # => shows MATCH: rank_bm25_topk's top score


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
