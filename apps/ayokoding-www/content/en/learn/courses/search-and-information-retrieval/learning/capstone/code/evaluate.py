# pyright: strict
"""Capstone Step 3: evaluate.py -- runs precision@k over a small relevance-judgment set
across two analyzer configs (co-22, co-23, co-09).

Verify: the metric changes as expected when a stemmer is toggled.
"""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Callable  # => from typing: Callable

from index import CORPUS, InvertedIndex  # => from index: CORPUS, InvertedIndex
from rank import rank_bm25_topk  # => from rank: rank_bm25_topk


def _cv_string(
    word: str,
) -> str:  # => porter (1980): reduce word to its consonant/vowel pattern, e.g. 'TROUBLE' -> 'CVCVCVC'
    """Porter (1980): reduce word to its consonant/vowel pattern, e.g. 'TROUBLE' -> 'CVCVCVC'."""
    return "".join(
        "V" if ch in "aeiou" else "C" for ch in word
    )  # => returns "".join("V" if ch in "aeiou" else "C" for ch in word)


def _measure(
    word: str,
) -> int:  # => porter's own m: the number of VC sequences in the [C](VC)^m[V] pattern
    """Porter's own m: the number of VC sequences in the [C](VC)^m[V] pattern."""
    cv: str = _cv_string(word)  # => cv = _cv_string(word)
    return cv.count("VC")  # => returns cv.count("VC")


def porter_stem(
    word: str,
) -> str:  # => a minimal Porter (1980) stemmer covering the common suffixes this corpus exercises
    """A minimal Porter (1980) stemmer covering the common suffixes this corpus exercises."""
    if (
        word.endswith("ing") and len(word) > 5 and _measure(word[:-3]) > 0
    ):  # => true when word.endswith("ing") and len(word) > 5 and _measure(...
        stem: str = word[
            :-3
        ]  # => co-09: Step 1b -- strip '-ing' when the stem has measure > 0
        return stem  # => returns stem
    if (
        word.endswith("es") and len(word) > 4
    ):  # => true when word.endswith("es") and len(word) > 4
        return word[:-2]  # => co-09: Step 1a-style -- strip the plural '-es'
    if (
        word.endswith("s") and not word.endswith("ss") and len(word) > 3
    ):  # => true when word.endswith("s") and not word.endswith("ss") and l...
        return word[:-1]  # => co-09: Step 1a -- strip a plain plural '-s'
    return word  # => already at its stem, or too short to safely reduce


def analyze_stemmed(
    text: str,
) -> list[
    str
]:  # => co-25: the SAME normalization as index.py's analyze(), PLUS Porter stemming
    """co-25: the SAME normalization as index.py's analyze(), PLUS Porter stemming."""
    working: str = text.lower()  # => working = text.lower()
    cleaned: str = "".join(
        ch if ch.isalnum() else " " for ch in working
    )  # => cleaned = "".join(ch if ch.isalnum() else " " for ch in w...
    tokens: list[str] = [
        str(t) for t in cleaned.split()
    ]  # => tokens = [str(t) for t in cleaned.split()]
    return [
        porter_stem(t) for t in tokens
    ]  # => co-09: the ONE extra stage vs the unstemmed analyzer


def build_index_with_analyzer(
    corpus: dict[int, str], analyzer_fn: Callable[[str], list[str]]
) -> InvertedIndex:  # => build an index using a GIVEN analyzer function -- lets the two configs share one builder
    """Build an index using a GIVEN analyzer function -- lets the two configs share one builder."""
    index = InvertedIndex()  # => co-01: starts empty, one per analyzer config
    for doc_id, text in corpus.items():  # => iterates one item at a time
        index.add(
            doc_id, analyzer_fn(text)
        )  # => co-25: whichever analyzer was passed in, applied uniformly
    return index  # => returns index


def precision_at_k(
    ranked: list[int], relevant: set[int], k: int
) -> float:  # => co-22: precision over only the top-k ranked results
    """co-22: precision over only the top-k ranked results."""
    top_k: list[int] = ranked[:k]  # => top k = ranked[:k]
    return (
        sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0
    )  # => returns sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0


def main() -> None:  # => defines main
    # co-23: doc 0, 1, 4, 6, 7 are ALL genuinely about search/information retrieval.
    relevant: set[int] = {0, 1, 4, 6, 7}  # => relevant = {0, 1, 4, 6, 7}
    query: str = (
        "searches"  # => a query form that appears VERBATIM in none of the 8 documents
    )

    unstemmed_index: InvertedIndex = build_index_with_analyzer(
        CORPUS, lambda t: [str(x) for x in t.lower().split()]
    )  # => unstemmed index = build_index_with_analyzer(CORPUS, lambda t: [st...
    stemmed_index: InvertedIndex = build_index_with_analyzer(
        CORPUS, analyze_stemmed
    )  # => stemmed index = build_index_with_analyzer(CORPUS, analyze_stemmed)

    unstemmed_ranking: list[int] = [
        d for d, _ in rank_bm25_topk(unstemmed_index, query, k=5)
    ]  # => co-22: WITHOUT stemming
    stemmed_query_tokens: list[str] = analyze_stemmed(
        query
    )  # => co-09: 'searches' stemmed, e.g. down toward 'search'
    stemmed_ranking: list[int] = [  # => stemmed ranking = [
        d
        for d, _ in rank_bm25_topk(
            stemmed_index, " ".join(stemmed_query_tokens), k=5
        )  # => part of this step's computation, continued from the line above
    ]  # => co-22: WITH stemming, query analyzed the SAME way as the index
    print(f"query {query!r} stems to {stemmed_query_tokens}")  # => shows query
    print(f"unstemmed ranking: {unstemmed_ranking}")  # => shows unstemmed ranking
    print(f"stemmed ranking:   {stemmed_ranking}")  # => shows stemmed ranking

    p_at_5_unstemmed: float = precision_at_k(
        unstemmed_ranking, relevant, k=5
    )  # => co-22: precision@5, no stemming
    p_at_5_stemmed: float = precision_at_k(
        stemmed_ranking, relevant, k=5
    )  # => co-22: precision@5, WITH stemming
    print(
        f"precision@5 (unstemmed): {p_at_5_unstemmed:.4f}"
    )  # => shows precision@5 (unstemmed)
    print(
        f"precision@5 (stemmed):   {p_at_5_stemmed:.4f}"
    )  # => shows precision@5 (stemmed)

    assert unstemmed_ranking == [], (
        "the UNSTEMMED analyzer must find ZERO candidates -- 'searches' matches no exact token"
    )  # => the UNSTEMMED analyzer must find ZERO candidates -- 'searches' matches no exact token
    assert p_at_5_unstemmed == 0.0, (
        "precision@5 must be 0.0 when there is nothing to retrieve at all"
    )  # => precision@5 must be 0.0 when there is nothing to retrieve at all
    assert p_at_5_stemmed > p_at_5_unstemmed, (
        "stemming must IMPROVE precision@5 by recovering the word-form mismatch"
    )  # => stemming must IMPROVE precision@5 by recovering the word-form mismatch
    print(
        f"MATCH: toggling the stemmer changed precision@5 from {p_at_5_unstemmed} to {p_at_5_stemmed} -- the metric responds as expected"
    )  # => shows MATCH: toggling the stemmer changed precision@5 from


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
