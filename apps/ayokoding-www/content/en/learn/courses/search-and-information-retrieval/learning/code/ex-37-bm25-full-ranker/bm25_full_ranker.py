# pyright: strict
"""Example 37: BM25 Full Ranker (co-16)."""

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


def rank_bm25(
    docs: dict[int, list[str]], query_terms: list[str]
) -> list[tuple[int, float]]:  # => defines rank bm25
    n_docs: int = len(docs)  # => this fixture's own size
    df: dict[str, int] = build_df(docs)  # => df = build_df(docs)
    total_len: int = sum(
        len(tokens) for tokens in docs.values()
    )  # => total len = sum(len(tokens) for tokens in docs.values())
    avgdl: float = (
        total_len / n_docs
    )  # => co-18: the corpus-wide average document length

    scores: dict[int, float] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        doc_tf: dict[str, int] = {}  # => starts empty, populated by the loop below
        for t in tokens:  # => iterates one item at a time
            doc_tf[t] = (
                doc_tf.get(t, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
        scores[doc_id] = bm25_score(
            query_terms, doc_tf, df, n_docs, float(len(tokens)), avgdl
        )  # => scores = bm25_score(query_terms, doc_tf, df, n_docs, flo...
    return sorted(
        scores.items(), key=lambda kv: (-kv[1], kv[0])
    )  # => returns sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "search",
            "engine",
            "index",
            "search",
            "engine",
        ],  # => strong match: BOTH terms, repeated
        1: ["search", "results", "page"],  # => weak match: only ONE term
        2: ["cooking", "recipe", "book"],  # => no match at all
        3: [
            "weather",
            "forecast",
            "today",
        ],  # => filler, no match -- keeps df(search)/df(engine) LOW relative to N
        4: [
            "news",
            "update",
            "daily",
        ],  # => filler, no match -- same reason: avoids a tiny-corpus idf sign flip
    }  # => opens/closes this multi-line literal
    query_terms: list[str] = [
        "search",
        "engine",
    ]  # => query terms = ["search", "engine"]
    ranking: list[tuple[int, float]] = rank_bm25(
        docs, query_terms
    )  # => co-16: the full BM25 ranking
    for doc_id, score in ranking:  # => iterates one item at a time
        print(f"doc {doc_id}: score={score:.4f}")  # => shows doc

    # An INDEPENDENT reference pass: recompute doc 0's score from scratch, a different way.
    n_docs = len(docs)  # => n docs = len(docs)
    df_ref: dict[str, int] = build_df(docs)  # => df ref = build_df(docs)
    avgdl_ref: float = (
        sum(len(t) for t in docs.values()) / n_docs
    )  # => avgdl ref = sum(len(t) for t in docs.values()) / n_docs
    ref_score_doc0: float = 0.0  # => ref score doc0 = 0.0
    for term in query_terms:  # => iterates one item at a time
        tf_doc0: int = docs[0].count(term)  # => tf doc0 = docs[0].count(term)
        if tf_doc0 > 0:  # => true when tf_doc0 > 0
            idf_ref: float = math.log(
                (n_docs - df_ref[term] + 0.5) / (df_ref[term] + 0.5)
            )  # => idf ref = math.log((n_docs - df_ref[term] + 0.5) / (df_re...
            B_ref: float = (1 - 0.75) + 0.75 * (
                len(docs[0]) / avgdl_ref
            )  # => B ref = (1 - 0.75) + 0.75 * (len(docs[0]) / avgdl_ref)
            ref_score_doc0 += (
                idf_ref * (tf_doc0 * 2.2) / (tf_doc0 + 1.2 * B_ref)
            )  # => part of this step's computation, continued from the line above

    assert ranking[0][0] == 0, (
        "doc 0 must rank first -- it matches both query terms, repeated"
    )  # => doc 0 must rank first -- it matches both query terms, repeated
    assert ranking[1][0] == 1, (
        "doc 1 must rank second -- it matches one query term, once"
    )  # => doc 1 must rank second -- it matches one query term, once
    assert ranking[0][1] > ranking[1][1] > 0, (
        "both matching docs must score strictly positive, doc 0 higher than doc 1"
    )  # => both matching docs must score strictly positive, doc 0 higher than doc 1
    assert math.isclose(ranking[0][1], ref_score_doc0, rel_tol=1e-9), (
        "doc 0's score must match the independent reference pass"
    )  # => doc 0's score must match the independent reference pass
    print(
        f"MATCH: doc 0 ranks first ({ranking[0][1]:.4f}), matching the independent reference computation ({ref_score_doc0:.4f})"
    )  # => shows MATCH: doc 0 ranks first (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
