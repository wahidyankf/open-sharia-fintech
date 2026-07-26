# pyright: strict
"""Capstone Step 1: index.py -- a typed inverted index with tokenization and persisted
postings, over a small real text corpus (co-01, co-02, co-03, co-04, co-06, co-07).

Verify: a boolean query returns the correct document set and `pyright` is clean.
"""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => stdlib JSON -- postings persistence to/from disk
from dataclasses import dataclass, field  # => from dataclasses: dataclass, field
from pathlib import Path  # => from pathlib: Path

# A small, real, in-repo text corpus: 8 short natural-language documents, some about
# search/information retrieval, some deliberately off-topic -- reused by every later
# capstone step (rank.py, evaluate.py, incremental.py) via `from index import CORPUS`.
CORPUS: dict[int, str] = {  # => CORPUS = {
    0: "Search engines index documents so users can find relevant information quickly.",  # => part of this step's computation, continued from the line above
    1: "A search engine ranks documents using term frequency and inverse document frequency.",  # => part of this step's computation, continued from the line above
    2: "Database indexes speed up query execution by avoiding full table scans.",  # => part of this step's computation, continued from the line above
    3: "Cooking a good stew requires patience, quality ingredients, and low heat.",  # => part of this step's computation, continued from the line above
    4: "Searching through a phone book by hand is slow compared to using an index.",  # => part of this step's computation, continued from the line above
    5: "The gardener watered the roses every morning before the sun grew hot.",  # => part of this step's computation, continued from the line above
    6: "Information retrieval systems rank search results by relevance to the query.",  # => part of this step's computation, continued from the line above
    7: "A quick search of the archive revealed the missing report from last year.",  # => part of this step's computation, continued from the line above
}  # => opens/closes this multi-line literal


def analyze(
    text: str, *, lowercase: bool = True
) -> list[
    str
]:  # => co-25: the analyzer -- lowercase (optional), then whitespace/punctuation-aware split
    """co-25: the analyzer -- lowercase (optional), then whitespace/punctuation-aware split."""
    working: str = (
        text.lower() if lowercase else text
    )  # => co-25: normalization stage, applied BEFORE tokenization
    cleaned: str = "".join(
        ch if ch.isalnum() else " " for ch in working
    )  # => co-06: strips punctuation into spaces
    return [
        str(t) for t in cleaned.split()
    ]  # => co-06: tokenization stage (widened from LiteralString for pyright)


@dataclass  # => part of this step's computation, continued from the line above
class InvertedIndex:  # => part of this step's computation, continued from the line above
    """co-01: term -> {doc_id: tf}, plus per-document lengths for BM25's length norm (co-18)."""

    postings: dict[str, dict[int, int]] = field(
        default_factory=lambda: {}
    )  # => co-01: the core inverted index
    doc_lengths: dict[int, int] = field(
        default_factory=lambda: {}
    )  # => co-18: needed later, by rank.py's BM25

    def add(
        self, doc_id: int, tokens: list[str]
    ) -> None:  # => co-29: index one document's tokens -- safe to call again later for incremental add
        """co-29: index one document's tokens -- safe to call again later for incremental add."""
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

    def query_and(
        self, terms: list[str]
    ) -> set[
        int
    ]:  # => co-06: boolean AND -- every term must be present in the returned documents
        """co-06: boolean AND -- every term must be present in the returned documents."""
        if not terms:  # => true when not terms
            return set()  # => returns set()
        result: set[int] = set(
            self.postings.get(terms[0], {}).keys()
        )  # => co-06: starts with the FIRST term's docs
        for term in terms[
            1:
        ]:  # => co-06: narrows the result with EVERY subsequent term
            result &= set(
                self.postings.get(term, {}).keys()
            )  # => part of this step's computation, continued from the line above
        return result  # => returns result

    def query_or(
        self, terms: list[str]
    ) -> set[int]:  # => co-07: boolean OR -- any one of the terms is enough to match
        """co-07: boolean OR -- any one of the terms is enough to match."""
        result: set[int] = (
            set()
        )  # => co-07: starts empty, grows with every matching term
        for term in terms:  # => iterates one item at a time
            result |= set(
                self.postings.get(term, {}).keys()
            )  # => part of this step's computation, continued from the line above
        return result  # => returns result

    def save(
        self, path: Path
    ) -> None:  # => co-30: persist postings + doc_lengths to JSON (string-keyed doc-ids, per Example 61)
        """co-30: persist postings + doc_lengths to JSON (string-keyed doc-ids, per Example 61)."""
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
    ) -> "InvertedIndex":  # => co-30: the exact inverse of save -- a fresh index, reconstructed entirely from disk
        """co-30: the exact inverse of save -- a fresh index, reconstructed entirely from disk."""
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )  # => payload = json.loads(path.read_text(encoding="utf-8"))
        index = InvertedIndex()  # => index = InvertedIndex()
        index.postings = {
            t: {int(d): tf for d, tf in dt.items()}
            for t, dt in payload["postings"].items()
        }  # => index = {t: {int(d): tf for d, tf in dt.items()} for t,...
        index.doc_lengths = {
            int(d): length for d, length in payload["doc_lengths"].items()
        }  # => index = {int(d): length for d, length in payload["doc_l...
        return index  # => returns index


def build_index(
    corpus: dict[int, str],
) -> (
    InvertedIndex
):  # => co-01: analyze every document and fold it into a fresh InvertedIndex
    """co-01: analyze every document and fold it into a fresh InvertedIndex."""
    index = InvertedIndex()  # => co-01: starts empty
    for doc_id, text in corpus.items():  # => iterates one item at a time
        index.add(
            doc_id, analyze(text)
        )  # => co-25: SAME analyzer at index time as at query time
    return index  # => returns index


def main() -> None:  # => defines main
    index: InvertedIndex = build_index(
        CORPUS
    )  # => co-01: the full 8-document capstone index
    print(
        f"indexed {len(CORPUS)} documents, {len(index.postings)} distinct terms"
    )  # => shows indexed

    and_hits: set[int] = index.query_and(
        ["search", "engine"]
    )  # => co-06: docs containing BOTH terms
    or_hits: set[int] = index.query_or(
        ["cooking", "gardener"]
    )  # => co-07: docs containing EITHER term
    print(
        f"AND('search', 'engine'): {sorted(and_hits)}"
    )  # => shows AND('search', 'engine')
    print(
        f"OR('cooking', 'gardener'): {sorted(or_hits)}"
    )  # => shows OR('cooking', 'gardener')

    hand_and: set[
        int
    ] = {  # => an INDEPENDENT recount, over the EXACT tokens (not a raw substring check)
        doc_id
        for doc_id, text in CORPUS.items()
        if {"search", "engine"}
        <= set(
            analyze(text)
        )  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    hand_or: set[int] = {  # => hand or = {
        doc_id
        for doc_id, text in CORPUS.items()
        if {"cooking", "gardener"}
        & set(
            analyze(text)
        )  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    assert and_hits == hand_and, (
        "AND query must match an independent recount of docs containing BOTH exact tokens"
    )  # => AND query must match an independent recount of docs containing BOTH exact tokens
    assert or_hits == hand_or, (
        "OR query must match an independent recount of docs containing EITHER exact token"
    )  # => OR query must match an independent recount of docs containing EITHER exact token
    assert and_hits == {1}, (
        "only doc 1 contains the EXACT tokens 'search' and 'engine' (doc 0 says 'engines', plural)"
    )  # => only doc 1 contains the EXACT tokens 'search' and 'engine' (doc 0 says 'engines', plural)
    assert or_hits == {3, 5}, (
        "exactly docs 3 and 5 mention 'cooking' or 'gardener'"
    )  # => exactly docs 3 and 5 mention 'cooking' or 'gardener'

    postings_path = Path(
        "postings.json"
    )  # => co-30: persisted for rank.py, evaluate.py, and incremental.py to reuse
    index.save(
        postings_path
    )  # => part of this step's computation, continued from the line above
    reloaded: InvertedIndex = InvertedIndex.load(
        postings_path
    )  # => co-30: round-trip check
    assert reloaded.postings == index.postings, (
        "reloaded postings must exactly match the original"
    )  # => reloaded postings must exactly match the original
    print(
        f"MATCH: boolean AND/OR queries agree with an independent recount, and the index persists+reloads exactly"
    )  # => shows MATCH: boolean AND/OR queries agree with an independent recount, and the index persists+reloads exactly


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
