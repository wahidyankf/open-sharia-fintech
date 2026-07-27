# pyright: strict
"""Example 80: Mini Search Engine (co-01, co-16, co-20, co-25)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import heapq  # => stdlib binary heap -- backs the size-k top-k selection
import json  # => stdlib JSON -- postings persistence to/from disk
import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing
from dataclasses import dataclass, field  # => from dataclasses: dataclass, field
from pathlib import Path  # => from pathlib: Path


def analyze(
    text: str,
) -> list[
    str
]:  # => co-25: the smallest useful analyzer -- lowercase, then whitespace-split
    """co-25: the smallest useful analyzer -- lowercase, then whitespace-split."""
    lowered: str = (
        text.lower()
    )  # => co-25: stage 1, a token filter's worth of normalization, applied early
    return [
        str(t) for t in lowered.split()
    ]  # => co-25: stage 2, tokenization (widened from LiteralString for pyright)


@dataclass  # => part of this step's computation, continued from the line above
class MiniSearchEngine:  # => part of this step's computation, continued from the line above
    """co-01: analyzer + inverted index + BM25 + top-k + persistence, behind one small API."""

    postings: dict[str, dict[int, int]] = field(
        default_factory=lambda: {}
    )  # => co-01: term -> {doc_id: tf}
    doc_lengths: dict[int, int] = field(
        default_factory=lambda: {}
    )  # => co-18: needed for BM25's length norm

    def add(
        self, doc_id: int, text: str
    ) -> None:  # => analyze raw text, then index the resulting tokens
        """Analyze raw text, then index the resulting tokens."""
        tokens: list[str] = analyze(text)  # => co-25: raw text -> normalized terms
        tf: dict[str, int] = {}  # => starts empty, populated by the loop below
        for t in tokens:  # => iterates one item at a time
            tf[t] = (
                tf.get(t, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
        for term, count in tf.items():  # => iterates one item at a time
            self.postings.setdefault(term, {})[doc_id] = (
                count  # => part of this step's computation, continued from the line above
            )
        self.doc_lengths[doc_id] = len(tokens)  # => self = len(tokens)

    def search(
        self, query: str, k: int = 5
    ) -> list[
        tuple[int, float]
    ]:  # => co-16 + co-20: BM25-rank every matching document, return the top k
        """co-16 + co-20: BM25-rank every matching document, return the top k."""
        query_terms: list[str] = analyze(
            query
        )  # => co-25: the query goes through the SAME analyzer as documents
        n_docs: int = len(self.doc_lengths)  # => this fixture's own size
        if n_docs == 0:  # => true when n_docs == 0
            return []  # => returns []
        avgdl: float = (
            sum(self.doc_lengths.values()) / n_docs
        )  # => co-18: this index's own average document length
        candidate_docs: set[int] = set()  # => candidate docs = set()
        for term in (
            query_terms
        ):  # => co-01: gathers every doc that contains AT LEAST ONE query term
            candidate_docs |= set(
                self.postings.get(term, {}).keys()
            )  # => part of this step's computation, continued from the line above

        scored: list[
            tuple[float, int]
        ] = []  # => co-16: (score, doc_id) pairs, before top-k selection
        for doc_id in candidate_docs:  # => iterates one item at a time
            score: float = 0.0  # => score = 0.0
            for term in query_terms:  # => iterates one item at a time
                if doc_id in self.postings.get(
                    term, {}
                ):  # => true when doc_id in self.postings.get(term, {})
                    tf: int = self.postings[term][
                        doc_id
                    ]  # => tf = self.postings[term][doc_id]
                    df: int = len(self.postings[term])  # => this fixture's own size
                    idf: float = math.log(
                        (n_docs - df + 0.5) / (df + 0.5)
                    )  # => co-16: BM25's own RSJ idf
                    B: float = (1 - 0.75) + 0.75 * (
                        self.doc_lengths[doc_id] / avgdl
                    )  # => B = (1 - 0.75) + 0.75 * (self.doc_lengths[doc_id] /...
                    score += (
                        idf * (tf * 2.2) / (tf + 1.2 * B)
                    )  # => part of this step's computation, continued from the line above
            scored.append((score, doc_id))  # => records this item, in order
        return [
            (doc_id, s) for s, doc_id in heapq.nlargest(k, scored)
        ]  # => co-20: top-k, not a full sort

    def save(
        self, path: Path
    ) -> None:  # => persist postings + doc_lengths to JSON (co-30's own string-keyed-int fix, applied here)
        """Persist postings + doc_lengths to JSON (co-30's own string-keyed-int fix, applied here)."""
        payload = {  # => payload = {
            "postings": {
                t: {str(d): tf for d, tf in dt.items()}
                for t, dt in self.postings.items()
            },  # => entry for 'postings'
            "doc_lengths": {
                str(d): length for d, length in self.doc_lengths.items()
            },  # => entry for 'doc_lengths'
        }  # => opens/closes this multi-line literal
        path.write_text(
            json.dumps(payload), encoding="utf-8"
        )  # => part of this step's computation, continued from the line above

    @staticmethod  # => part of this step's computation, continued from the line above
    def load(
        path: Path,
    ) -> "MiniSearchEngine":  # => the exact inverse of save -- a FRESH engine, reconstructed entirely from disk
        """The exact inverse of save -- a FRESH engine, reconstructed entirely from disk."""
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )  # => payload = json.loads(path.read_text(encoding="utf-8"))
        engine = MiniSearchEngine()  # => engine = MiniSearchEngine()
        engine.postings = {
            t: {int(d): tf for d, tf in dt.items()}
            for t, dt in payload["postings"].items()
        }  # => engine = {t: {int(d): tf for d, tf in dt.items()} for t,...
        engine.doc_lengths = {
            int(d): length for d, length in payload["doc_lengths"].items()
        }  # => engine = {int(d): length for d, length in payload["doc_l...
        return engine  # => returns engine


def main() -> None:  # => defines main
    engine = MiniSearchEngine()  # => co-01: an empty mini search engine
    engine.add(
        0, "search engines rank documents by relevance"
    )  # => part of this step's computation, continued from the line above
    engine.add(
        1, "cooking recipes for a quick dinner"
    )  # => part of this step's computation, continued from the line above
    engine.add(
        2, "search engine ranking algorithms explained"
    )  # => part of this step's computation, continued from the line above

    results_before_persist: list[tuple[int, float]] = engine.search(
        "search engine", k=2
    )  # => co-16, co-20: pre-persistence
    print(
        f"results before persistence: {results_before_persist}"
    )  # => shows results before persistence

    path = Path("mini_search_engine.json")  # => co-30: a real file on disk
    engine.save(path)  # => co-30: persist the built index
    reloaded_engine = MiniSearchEngine.load(
        path
    )  # => co-30: a FRESH object, built ONLY from the saved file
    results_after_reload: list[tuple[int, float]] = reloaded_engine.search(
        "search engine", k=2
    )  # => the SAME query, post-reload
    print(
        f"results after reload: {results_after_reload}"
    )  # => shows results after reload

    assert results_before_persist[0][0] in (0, 2), (
        "the top result must be one of the two docs mentioning 'search'/'engine'"
    )  # => the top result must be one of the two docs mentioning 'search'/'engine'
    assert [d for d, _ in results_before_persist] == [
        d for d, _ in results_after_reload
    ], (
        "reload must return docs in the SAME order"
    )  # => reload must return docs in the SAME order
    print(
        f"MATCH: the reloaded engine returns identical ranked results to the original, end to end"
    )  # => shows MATCH: the reloaded engine returns identical ranked results to the original, end to end


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
