# pyright: strict
"""Example 63: Delta-Encode Postings (co-30)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def delta_encode(
    sorted_doc_ids: list[int],
) -> list[
    int
]:  # => replace each doc-id with the GAP since the previous one (first id is its own gap)
    """Replace each doc-id with the GAP since the previous one (first id is its own gap)."""
    if not sorted_doc_ids:  # => true when not sorted_doc_ids
        return []  # => returns []
    deltas: list[int] = [
        sorted_doc_ids[0]
    ]  # => co-30: the FIRST id is stored as-is, there is no "previous"
    for i in range(1, len(sorted_doc_ids)):  # => every SUBSEQUENT id, one gap at a time
        deltas.append(
            sorted_doc_ids[i] - sorted_doc_ids[i - 1]
        )  # => records this item, in order
    return deltas  # => returns deltas


def delta_decode(
    deltas: list[int],
) -> list[
    int
]:  # => the exact inverse: running sum of the gaps reconstructs the original sorted ids
    """The exact inverse: running sum of the gaps reconstructs the original sorted ids."""
    if not deltas:  # => true when not deltas
        return []  # => returns []
    doc_ids: list[int] = [deltas[0]]  # => the first delta IS the first doc-id
    for gap in deltas[1:]:  # => every SUBSEQUENT gap, added cumulatively
        doc_ids.append(doc_ids[-1] + gap)  # => records this item, in order
    return doc_ids  # => returns doc_ids


def packed_size(
    values: list[int],
) -> int:  # => a 1-byte-per-value encoding when every value fits in a byte, else 4 bytes -- a size proxy
    """A 1-byte-per-value encoding when every value fits in a byte, else 4 bytes -- a size proxy."""
    return sum(
        1 if v < 256 else 4 for v in values
    )  # => co-30: SMALL deltas pack into 1 byte, large raw ids need 4


def main() -> None:  # => defines main
    dense_doc_ids: list[int] = [
        1000,
        1002,
        1005,
        1009,
        1014,
        1020,
    ]  # => CLUSTERED doc-ids -- small gaps between them

    deltas: list[int] = delta_encode(
        dense_doc_ids
    )  # => co-30: [1000, 2, 3, 4, 5, 6] -- mostly tiny numbers
    decoded: list[int] = delta_decode(
        deltas
    )  # => co-30: reconstructs the original list, exactly
    print(f"original doc-ids: {dense_doc_ids}")  # => shows original doc-ids
    print(f"deltas:           {deltas}")  # => shows deltas
    print(f"decoded:          {decoded}")  # => shows decoded

    raw_size: int = packed_size(
        dense_doc_ids
    )  # => how many bytes the RAW ids would need
    delta_size: int = packed_size(deltas)  # => how many bytes the DELTAS need
    print(
        f"raw size: {raw_size} bytes   delta size: {delta_size} bytes"
    )  # => shows raw size

    assert decoded == dense_doc_ids, (
        "delta_decode(delta_encode(x)) must reconstruct x exactly"
    )  # => delta_decode(delta_encode(x)) must reconstruct x exactly
    assert delta_size < raw_size, (
        "delta-encoded CLUSTERED ids must pack smaller than the raw ids"
    )  # => delta-encoded CLUSTERED ids must pack smaller than the raw ids
    print(
        f"MATCH: exact round-trip, and delta encoding saves {raw_size - delta_size} bytes on this clustered posting list"
    )  # => shows MATCH: exact round-trip, and delta encoding saves


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
