# pyright: strict
"""Example 62: Persist Binary (co-30)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => stdlib JSON -- postings persistence to/from disk
import struct  # => stdlib fixed-width binary packing -- the compact postings encoding
from pathlib import Path  # => from pathlib: Path


def save_postings_binary(
    postings: dict[str, dict[int, int]], path: Path
) -> None:  # => pack each term's postings as: term length, term bytes, count, then (doc_id, tf) pairs
    """Pack each term's postings as: term length, term bytes, count, then (doc_id, tf) pairs."""
    with path.open("wb") as f:  # => co-30: BINARY mode -- raw bytes, not text
        for term, doc_tfs in postings.items():  # => iterates one item at a time
            term_bytes: bytes = term.encode(
                "utf-8"
            )  # => the term itself, UTF-8 encoded
            f.write(
                struct.pack("<H", len(term_bytes))
            )  # => co-30: 2-byte unsigned length prefix
            f.write(
                term_bytes
            )  # => part of this step's computation, continued from the line above
            f.write(
                struct.pack("<H", len(doc_tfs))
            )  # => how many (doc_id, tf) pairs follow
            for doc_id, tf in sorted(
                doc_tfs.items()
            ):  # => co-30: SORTED -- a stable, deterministic order
                f.write(
                    struct.pack("<II", doc_id, tf)
                )  # => co-30: two 4-byte unsigned ints, packed


def load_postings_binary(
    path: Path,
) -> dict[
    str, dict[int, int]
]:  # => the exact inverse of save_postings_binary, reading the same fixed layout back
    """The exact inverse of save_postings_binary, reading the same fixed layout back."""
    postings: dict[
        str, dict[int, int]
    ] = {}  # => co-30: rebuilt term -> {doc_id: tf} structure
    with path.open(
        "rb"
    ) as f:  # => part of this step's computation, continued from the line above
        while True:  # => loops while the condition holds
            len_bytes: bytes = f.read(2)  # => the 2-byte term-length prefix, or EOF
            if not len_bytes:  # => true when not len_bytes
                break  # => part of this step's computation, continued from the line above
            (term_len,) = struct.unpack(
                "<H", len_bytes
            )  # => part of this step's computation, continued from the line above
            term: str = f.read(term_len).decode(
                "utf-8"
            )  # => the term itself, decoded back to str
            (pair_count,) = struct.unpack(
                "<H", f.read(2)
            )  # => part of this step's computation, continued from the line above
            doc_tfs: dict[int, int] = {}  # => starts empty, populated by the loop below
            for _ in range(
                pair_count
            ):  # => reads EXACTLY pair_count (doc_id, tf) pairs
                doc_id, tf = struct.unpack(
                    "<II", f.read(8)
                )  # => part of this step's computation, continued from the line above
                doc_tfs[doc_id] = tf  # => stores this computed value under its key
            postings[term] = doc_tfs  # => stores this computed value under its key
    return postings  # => returns postings


def main() -> None:  # => defines main
    postings: dict[str, dict[int, int]] = {
        "search": {0: 2, 1: 1},
        "engine": {0: 1},
        "cooking": {2: 1},
    }  # => postings = {"search": {0: 2, 1: 1}, "engine": {0: 1}, "coo...
    binary_path = Path("postings.bin")  # => co-30: the compact binary file
    json_path = Path(
        "postings_compare.json"
    )  # => a JSON version of the SAME data, for a fair size comparison

    save_postings_binary(postings, binary_path)  # => co-30: writes the compact encoding
    json_path.write_text(
        json.dumps(
            {t: {str(d): tf for d, tf in dt.items()} for t, dt in postings.items()}
        ),
        encoding="utf-8",
    )  # => part of this step's computation, continued from the line above

    reloaded: dict[str, dict[int, int]] = load_postings_binary(
        binary_path
    )  # => co-30: reads the binary file back
    binary_size: int = (
        binary_path.stat().st_size
    )  # => binary size = binary_path.stat().st_size
    json_size: int = json_path.stat().st_size  # => json size = json_path.stat().st_size
    print(
        f"binary size: {binary_size} bytes   json size: {json_size} bytes"
    )  # => shows binary size

    assert reloaded == postings, (
        "the binary round-trip must reproduce the EXACT original postings"
    )  # => the binary round-trip must reproduce the EXACT original postings
    assert binary_size < json_size, (
        "the compact binary encoding must be SMALLER than the JSON text encoding"
    )  # => the compact binary encoding must be SMALLER than the JSON text encoding
    print(
        f"MATCH: binary round-trips exactly and is {json_size - binary_size} bytes smaller than JSON for the same data"
    )  # => shows MATCH: binary round-trips exactly and is


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
