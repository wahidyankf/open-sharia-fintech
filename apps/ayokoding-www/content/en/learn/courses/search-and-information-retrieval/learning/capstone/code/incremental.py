# pyright: strict
"""Capstone Step 4: incremental.py -- adds a new document to the built index without a
full rebuild (co-29).

Verify: it becomes findable and its BM25 score is consistent with a from-scratch rebuild.
"""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing

from index import (
    CORPUS,
    InvertedIndex,
    analyze,
    build_index,
)  # => from index: CORPUS, InvertedIndex, analyze, build_index
from rank import bm25_score  # => from rank: bm25_score


def main() -> None:  # => defines main
    index: InvertedIndex = build_index(
        CORPUS
    )  # => co-01: the already-built 8-document capstone index
    new_doc_id: int = 8  # => the next available doc-id
    new_doc_text: str = "A crawler indexes the web so a search engine can serve fast queries."  # => new doc text = "A crawler indexes the web so a search engine c...

    before: set[int] = index.query_and(
        ["crawler"]
    )  # => co-29: the term does not exist YET
    print(
        f"query_and(['crawler']) BEFORE incremental add: {sorted(before)}"
    )  # => shows query_and(['crawler']) BEFORE incremental add
    assert before == set(), (
        "'crawler' must be unfindable before the new document is added"
    )  # => 'crawler' must be unfindable before the new document is added

    index.add(
        new_doc_id, analyze(new_doc_text)
    )  # => co-29: incremental add -- NO rebuild of docs 0-7
    after: set[int] = index.query_and(
        ["crawler"]
    )  # => co-29: the SAME index object, queried again
    print(
        f"query_and(['crawler']) AFTER incremental add: {sorted(after)}"
    )  # => shows query_and(['crawler']) AFTER incremental add
    assert after == {new_doc_id}, (
        "'crawler' must be immediately findable in the newly added doc 8"
    )  # => 'crawler' must be immediately findable in the newly added doc 8

    # Consistency check: the incremental index's BM25 scores for a shared query must match
    # a FROM-SCRATCH rebuild that includes doc 8 from the very start.
    full_corpus: dict[int, str] = {
        **CORPUS,
        new_doc_id: new_doc_text,
    }  # => the SAME final document set
    rebuilt: InvertedIndex = build_index(
        full_corpus
    )  # => co-29: a from-scratch reference build

    query_terms: list[str] = analyze(
        "search engine"
    )  # => the query BOTH indexes will be scored against
    incremental_avgdl: float = sum(index.doc_lengths.values()) / len(
        index.doc_lengths
    )  # => co-18: this index's own avgdl
    rebuilt_avgdl: float = sum(rebuilt.doc_lengths.values()) / len(
        rebuilt.doc_lengths
    )  # => co-18: the rebuild's own avgdl
    assert math.isclose(incremental_avgdl, rebuilt_avgdl), (
        "avgdl must match between the incremental index and the rebuild"
    )  # => avgdl must match between the incremental index and the rebuild

    for doc_id in full_corpus:  # => checks EVERY document, not just the newly added one
        incremental_score: float = bm25_score(
            index, query_terms, doc_id, incremental_avgdl
        )  # => incremental score = bm25_score(index, query_terms, doc_id, incremen...
        rebuilt_score: float = bm25_score(
            rebuilt, query_terms, doc_id, rebuilt_avgdl
        )  # => rebuilt score = bm25_score(rebuilt, query_terms, doc_id, rebuil...
        assert math.isclose(incremental_score, rebuilt_score, rel_tol=1e-9), (
            f"doc {doc_id}: incremental BM25 score must match the rebuild"
        )  # => doc {doc_id}: incremental BM25 score must match the rebuild

    print(
        f"incremental doc 8 BM25 score: {bm25_score(index, query_terms, new_doc_id, incremental_avgdl):.6f}"
    )  # => shows incremental doc 8 BM25 score
    print(
        f"rebuilt     doc 8 BM25 score: {bm25_score(rebuilt, query_terms, new_doc_id, rebuilt_avgdl):.6f}"
    )  # => shows rebuilt     doc 8 BM25 score
    print(
        f"MATCH: doc 8 is immediately findable, and every document's BM25 score matches a full from-scratch rebuild"
    )  # => shows MATCH: doc 8 is immediately findable, and every document's BM25 score matches a full from-scratch rebuild


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
