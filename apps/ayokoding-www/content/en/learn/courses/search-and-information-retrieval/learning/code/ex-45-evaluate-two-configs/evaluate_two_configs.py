# pyright: strict
"""Example 45: Evaluate Two Configs (co-22, co-23)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def bm25_idf(
    term_df: int, n_docs: int
) -> float:  # => bM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5)) -- distinct from plain log(N/df)
    """BM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5)) -- distinct from plain log(N/df)."""
    return math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => returns math.log((n_docs - term_df + 0.5) / (term_df + 0.5))


def bm25_term_weight(  # => defines bm25 term weight
    tf: int,
    term_df: int,
    n_docs: int,
    dl: float,
    avgdl: float,
    *,
    k1: float = 1.2,
    b: float = 0.75,  # => part of this step's computation, continued from the line above
) -> float:  # => part of this step's computation, continued from the line above
    """One query term's BM25 contribution: RSJ idf * saturating tf * length normalization."""
    idf: float = bm25_idf(term_df, n_docs)  # => idf = bm25_idf(term_df, n_docs)
    length_norm: float = (1 - b) + b * (
        dl / avgdl
    )  # => co-18: B -- 1.0 at average length, >1 for long docs
    return (
        idf * (tf * (k1 + 1)) / (tf + k1 * length_norm)
    )  # => co-17: the k1-saturated, B-normalized term score


def bm25_score(  # => defines bm25 score
    query_terms: list[
        str
    ],  # => part of this step's computation, continued from the line above
    doc_tf: dict[
        str, int
    ],  # => part of this step's computation, continued from the line above
    df: dict[
        str, int
    ],  # => part of this step's computation, continued from the line above
    n_docs: int,  # => part of this step's computation, continued from the line above
    dl: float,  # => part of this step's computation, continued from the line above
    avgdl: float,  # => part of this step's computation, continued from the line above
    *,  # => part of this step's computation, continued from the line above
    k1: float = 1.2,  # => k1 = 1.2,
    b: float = 0.75,  # => b = 0.75,
) -> float:  # => part of this step's computation, continued from the line above
    """Sum bm25_term_weight over every query term the document actually contains."""
    total: float = 0.0  # => total = 0.0
    for term in query_terms:  # => iterates one item at a time
        if term in doc_tf:  # => true when term in doc_tf
            total += bm25_term_weight(
                doc_tf[term], df.get(term, 0), n_docs, dl, avgdl, k1=k1, b=b
            )  # => part of this step's computation, continued from the line above
    return total  # => returns total


def build_df(docs: dict[int, list[str]]) -> dict[str, int]:  # => defines build df
    df: dict[str, int] = {}  # => starts empty, populated by the loop below
    for tokens in docs.values():  # => iterates one item at a time
        for term in set(tokens):  # => iterates one item at a time
            df[term] = (
                df.get(term, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
    return df  # => returns df


def rank_tfidf(
    docs: dict[int, list[str]], query_terms: list[str]
) -> list[int]:  # => defines rank tfidf
    n_docs: int = len(docs)  # => this fixture's own size
    df: dict[str, int] = build_df(docs)  # => df = build_df(docs)
    scores: dict[int, float] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        tf: dict[str, int] = {}  # => starts empty, populated by the loop below
        for t in tokens:  # => iterates one item at a time
            tf[t] = (
                tf.get(t, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
        scores[doc_id] = sum(
            tf[t] * math.log(n_docs / df[t]) for t in query_terms if t in tf
        )  # => scores = sum(tf[t] * math.log(n_docs / df[t]) for t in q...
    return [
        doc_id for doc_id, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    ]  # => returns [doc_id for doc_id, _ in sorted(scores.items(), key=lambd...


def rank_bm25_docs(
    docs: dict[int, list[str]], query_terms: list[str]
) -> list[int]:  # => defines rank bm25 docs
    n_docs: int = len(docs)  # => this fixture's own size
    df: dict[str, int] = build_df(docs)  # => df = build_df(docs)
    avgdl: float = (
        sum(len(t) for t in docs.values()) / n_docs
    )  # => avgdl = sum(len(t) for t in docs.values()) / n_docs
    scores: dict[int, float] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        tf: dict[str, int] = {}  # => starts empty, populated by the loop below
        for t in tokens:  # => iterates one item at a time
            tf[t] = (
                tf.get(t, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
        scores[doc_id] = bm25_score(
            query_terms, tf, df, n_docs, float(len(tokens)), avgdl
        )  # => scores = bm25_score(query_terms, tf, df, n_docs, float(l...
    return [
        doc_id for doc_id, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    ]  # => returns [doc_id for doc_id, _ in sorted(scores.items(), key=lambd...


def precision_at_k(
    ranked: list[int], relevant: set[int], k: int
) -> float:  # => defines precision at k
    top_k: list[int] = ranked[:k]  # => top k = ranked[:k]
    return (
        sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0
    )  # => returns sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: ["search", "engine"] * 5
        + ["content"]
        * 40,  # => KEYWORD-STUFFED: 5x each term padded into a 50-token doc
        1: [
            "search",
            "engine",
            "index",
            "ranking",
        ],  # => balanced, on-topic, each term ONCE
        2: ["cooking", "recipe"],  # => off-topic
        3: [
            "weather",
            "forecast",
            "today",
        ],  # => filler, off-topic -- keeps df(search)/df(engine) LOW relative to N
        4: [
            "news",
            "update",
            "daily",
        ],  # => filler, off-topic -- same reason: avoids a tiny-corpus idf sign flip
    }  # => opens/closes this multi-line literal
    query_terms: list[str] = [
        "search",
        "engine",
    ]  # => query terms = ["search", "engine"]
    qrels: dict[int, bool] = {
        0: False,
        1: True,
        2: False,
        3: False,
        4: False,
    }  # => co-23: doc 1 is the ONE truly relevant result
    relevant: set[int] = {
        doc_id for doc_id, is_rel in qrels.items() if is_rel
    }  # => relevant = {doc_id for doc_id, is_rel in qrels.items() if ...

    tfidf_ranking: list[int] = rank_tfidf(
        docs, query_terms
    )  # => co-22: tf-idf's ranked order
    bm25_ranking: list[int] = rank_bm25_docs(
        docs, query_terms
    )  # => co-22: BM25's ranked order
    p1_tfidf: float = precision_at_k(
        tfidf_ranking, relevant, k=1
    )  # => precision@1 for each config
    p1_bm25: float = precision_at_k(
        bm25_ranking, relevant, k=1
    )  # => p1 bm25 = precision_at_k(bm25_ranking, relevant, k=1)
    print(
        f"tf-idf ranking: {tfidf_ranking}  precision@1={p1_tfidf:.4f}"
    )  # => shows tf-idf ranking
    print(
        f"bm25 ranking:   {bm25_ranking}   precision@1={p1_bm25:.4f}"
    )  # => shows bm25 ranking

    assert tfidf_ranking[0] == 0, (
        "tf-idf's unbounded tf lets the repetitive doc 0 rank first (a hand-tallied fact of this fixture)"
    )  # => tf-idf's unbounded tf lets the repetitive doc 0 rank first (a hand-tallied fact of this fixture)
    assert bm25_ranking[0] == 1, (
        "BM25's saturation lets the balanced, truly relevant doc 1 rank first instead"
    )  # => BM25's saturation lets the balanced, truly relevant doc 1 rank first instead
    assert p1_bm25 > p1_tfidf, (
        "BM25 must score HIGHER precision@1 than tf-idf on this fixture"
    )  # => BM25 must score HIGHER precision@1 than tf-idf on this fixture
    print(
        f"MATCH: BM25's precision@1 ({p1_bm25}) beats tf-idf's ({p1_tfidf}) -- saturation avoided the keyword-stuffed doc"
    )  # => shows MATCH: BM25's precision@1 (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
