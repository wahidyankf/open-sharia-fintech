# pyright: strict
"""Example 61: Persist JSON (co-30)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => stdlib JSON -- postings persistence to/from disk
from pathlib import Path  # => from pathlib: Path


def save_postings_json(
    postings: dict[str, dict[int, int]], path: Path
) -> None:  # => jSON object keys must be strings -- convert every int doc_id to str before dumping
    """JSON object keys must be strings -- convert every int doc_id to str before dumping."""
    json_safe: dict[
        str, dict[str, int]
    ] = {  # => co-30: term -> {doc_id AS STRING -> tf}
        term: {str(doc_id): tf for doc_id, tf in doc_tfs.items()}
        for term, doc_tfs in postings.items()  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    path.write_text(
        json.dumps(json_safe), encoding="utf-8"
    )  # => part of this step's computation, continued from the line above


def load_postings_json(
    path: Path,
) -> dict[
    str, dict[int, int]
]:  # => reverse the string-key conversion, restoring int doc_ids
    """Reverse the string-key conversion, restoring int doc_ids."""
    json_safe: dict[str, dict[str, int]] = json.loads(
        path.read_text(encoding="utf-8")
    )  # => json safe = json.loads(path.read_text(encoding="utf-8"))
    return {
        term: {int(doc_id): tf for doc_id, tf in doc_tfs.items()}
        for term, doc_tfs in json_safe.items()
    }  # => co-30: str -> int, restored


def main() -> None:  # => defines main
    postings: dict[str, dict[int, int]] = {  # => a small in-memory index to persist
        "search": {0: 2, 1: 1},  # => entry for 'search'
        "engine": {0: 1},  # => entry for 'engine'
        "cooking": {2: 1},  # => entry for 'cooking'
    }  # => opens/closes this multi-line literal
    path = Path(
        "postings.json"
    )  # => co-30: a real file on disk, in this example's own directory
    save_postings_json(postings, path)  # => co-30: writes the JSON-safe form to disk
    reloaded: dict[str, dict[int, int]] = load_postings_json(
        path
    )  # => co-30: reads it back, restoring int keys
    print(f"original:  {postings}")  # => shows original
    print(f"reloaded:  {reloaded}")  # => shows reloaded
    print(f"file size: {path.stat().st_size} bytes")  # => shows file size

    assert reloaded == postings, (
        "the reloaded postings must be IDENTICAL to the original in-memory postings"
    )  # => the reloaded postings must be IDENTICAL to the original in-memory postings
    assert isinstance(next(iter(reloaded["search"])), int), (
        "reloaded doc-ids must be int, not str, after loading"
    )  # => reloaded doc-ids must be int, not str, after loading
    print(
        f"MATCH: postings round-tripped through JSON exactly, with doc-ids correctly restored to int"
    )  # => shows MATCH: postings round-tripped through JSON exactly, with doc-ids correctly restored to int


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
