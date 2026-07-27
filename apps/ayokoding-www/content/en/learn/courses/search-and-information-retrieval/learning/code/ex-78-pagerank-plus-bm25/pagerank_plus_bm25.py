# pyright: strict
"""Example 78: PageRank + BM25 (co-36)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def pagerank(
    links: dict[int, list[int]], damping: float = 0.85, iterations: int = 100
) -> dict[int, float]:  # => defines pagerank
    nodes: list[int] = list(links)  # => nodes = list(links)
    n: int = len(nodes)  # => this fixture's own size
    scores: dict[int, float] = {
        node: 1.0 / n for node in nodes
    }  # => scores = {node: 1.0 / n for node in nodes}
    for _ in range(iterations):  # => iterates one item at a time
        new_scores: dict[int, float] = {
            node: (1 - damping) / n for node in nodes
        }  # => new scores = {node: (1 - damping) / n for node in nodes}
        for node, outlinks in links.items():  # => iterates one item at a time
            if not outlinks:  # => true when not outlinks
                continue  # => part of this step's computation, continued from the line above
            share: float = scores[node] / len(
                outlinks
            )  # => share = scores[node] / len(outlinks)
            for target in outlinks:  # => iterates one item at a time
                new_scores[target] += (
                    damping * share
                )  # => part of this step's computation, continued from the line above
        scores = new_scores  # => scores = new_scores
    return scores  # => returns scores


def bm25_term_score(
    tf: int,
    term_df: int,
    n_docs: int,
    dl: float,
    avgdl: float,
    k1: float = 1.2,
    b: float = 0.75,
) -> float:  # => defines bm25 term score
    idf: float = math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => idf = math.log((n_docs - term_df + 0.5) / (term_df + ...
    length_norm: float = (1 - b) + b * (
        dl / avgdl
    )  # => length norm = (1 - b) + b * (dl / avgdl)
    return (
        idf * (tf * (k1 + 1)) / (tf + k1 * length_norm)
    )  # => returns idf * (tf * (k1 + 1)) / (tf + k1 * length_norm)


def combined_rank(
    bm25_scores: dict[int, float],
    link_scores: dict[int, float],
    link_weight: float = 5.0,
) -> list[
    int
]:  # => a simple linear combination: BM25 relevance PLUS a scaled link-authority score
    """A simple linear combination: BM25 relevance PLUS a scaled link-authority score."""
    combined: dict[
        int, float
    ] = {  # => co-36: term relevance and link authority, added into ONE score
        doc_id: bm25_scores.get(doc_id, 0.0)
        + link_weight * link_scores.get(doc_id, 0.0)
        for doc_id in bm25_scores  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    return sorted(
        combined, key=lambda d: -combined[d]
    )  # => returns sorted(combined, key=lambda d: -combined[d])


def main() -> None:  # => defines main
    # doc 0: a well-linked, MARGINALLY relevant page; doc 1: an orphan (unlinked), SLIGHTLY more relevant.
    bm25_scores: dict[int, float] = {
        0: 1.0,
        1: 1.1,
    }  # => doc 1 is the SLIGHTLY better term match on its own
    links: dict[int, list[int]] = {
        0: [],
        1: [],
        2: [0],
        3: [0],
        4: [0],
    }  # => co-36: three OTHER pages all link to doc 0
    link_scores: dict[int, float] = pagerank(
        links
    )  # => co-36: doc 0's link authority should dominate

    bm25_only_ranking: list[int] = sorted(
        bm25_scores, key=lambda d: -bm25_scores[d]
    )  # => term relevance ALONE
    final_ranking: list[int] = combined_rank(
        bm25_scores, link_scores
    )  # => co-36: term relevance PLUS link authority
    print(f"link scores: {link_scores}")  # => shows link scores
    print(f"BM25-only ranking: {bm25_only_ranking}")  # => shows BM25-only ranking
    print(f"combined ranking:  {final_ranking}")  # => shows combined ranking

    assert bm25_only_ranking[0] == 1, (
        "on TERM RELEVANCE alone, the marginally-better-matching orphan (doc 1) must rank first"
    )  # => on TERM RELEVANCE alone, the marginally-better-matching orphan (doc 1) must rank first
    assert final_ranking[0] == 0, (
        "once LINK AUTHORITY is folded in, the well-linked doc 0 must overtake the orphan"
    )  # => once LINK AUTHORITY is folded in, the well-linked doc 0 must overtake the orphan
    print(
        f"MATCH: doc 1 wins on relevance alone, but the well-linked doc 0 wins once link authority is combined in"
    )  # => shows MATCH: doc 1 wins on relevance alone, but the well-linked doc 0 wins once link authority is combined in


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
