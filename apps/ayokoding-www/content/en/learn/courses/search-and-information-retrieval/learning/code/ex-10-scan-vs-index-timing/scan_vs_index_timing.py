# pyright: strict
"""Example 10: Scan vs Index Timing (co-01)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => stdlib timer -- wall-clock measurement, not a benchmark micro-op


def build_docs(
    n: int,
) -> list[
    str
]:  # => build n synthetic documents; only ONE additional document contains the needle term
    """Build n synthetic documents; only ONE additional document contains the needle term."""
    docs: list[str] = [
        f"filler words about topic number {i} nothing relevant here" for i in range(n)
    ]  # => n non-matching docs
    docs.append(
        "this final document mentions the needle term explicitly"
    )  # => the ONE doc containing "needle"
    return docs  # => returns docs


def scan_time(
    docs: list[str], term: str
) -> float:  # => time a naive substring scan across every document -- O(N) per query
    """Time a naive substring scan across every document -- O(N) per query."""
    start: float = time.perf_counter()  # => wall-clock start
    _ = [
        d for d in docs if term in d
    ]  # => co-01: must touch EVERY doc, no matter where the match is
    return time.perf_counter() - start  # => elapsed seconds for this one scan


def index_lookup_time(
    index: dict[str, list[int]], term: str
) -> (
    float
):  # => time a single dict lookup against a pre-built inverted index -- O(1) amortized
    """Time a single dict lookup against a pre-built inverted index -- O(1) amortized."""
    start: float = time.perf_counter()  # => wall-clock start
    _ = index.get(term, [])  # => co-01: a single hash lookup, regardless of corpus size
    return time.perf_counter() - start  # => elapsed seconds for this one lookup


def main() -> None:  # => defines main
    sizes: tuple[int, ...] = (
        2_000,
        8_000,
        32_000,
    )  # => geometrically growing corpus sizes
    scan_seconds_by_n: dict[
        int, float
    ] = {}  # => remembers each N's own best scan time, for the check below
    for n in sizes:  # => iterates one item at a time
        docs: list[str] = build_docs(n)  # => n+1 documents total
        index: dict[str, list[int]] = {
            "needle": [n]
        }  # => the pre-built index already knows WHERE "needle" is
        scan_seconds: float = min(
            scan_time(docs, "needle") for _ in range(5)
        )  # => best of 5, reduces noise
        index_seconds: float = min(
            index_lookup_time(index, "needle") for _ in range(5)
        )  # => best of 5
        scan_seconds_by_n[n] = scan_seconds  # => stored for the growth check below
        ratio: float = (
            scan_seconds / index_seconds if index_seconds > 0 else float("inf")
        )  # => how much slower the scan is
        print(
            f"N={n:>6}: scan={scan_seconds * 1e6:9.1f}us  index={index_seconds * 1e6:8.3f}us  ratio={ratio:8.0f}x"
        )  # => shows N=

    assert scan_seconds_by_n[sizes[-1]] > scan_seconds_by_n[sizes[0]], (
        "scan time must rise as N grows"
    )  # => scan time must rise as N grows
    print(  # => prints this step's result
        f"MATCH: scan time rises with N ({scan_seconds_by_n[sizes[0]] * 1e6:.1f}us -> "  # => continues the f-string/message started on the prior line
        f"{scan_seconds_by_n[sizes[-1]] * 1e6:.1f}us) while an index lookup stays a flat, single hash lookup"  # => continues the f-string/message started on the prior line
    )  # => opens/closes this multi-line literal


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
