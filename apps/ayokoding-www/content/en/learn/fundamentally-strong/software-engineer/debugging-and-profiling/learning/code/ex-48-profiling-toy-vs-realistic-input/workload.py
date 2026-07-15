"""Example 48: a workload whose bottleneck DEPENDS on input scale.

`dedupe_naive` is O(n^2) (list membership); `normalize` is O(n) but has a higher
per-item constant (a regex substitution). At 100 items the O(n) function with the
expensive constant dominates; at 1,000,000 items the O(n^2) function dominates so
badly it swamps everything else. Profiling only at toy scale would send you
optimizing the wrong function.
"""

from __future__ import annotations

import re

_WHITESPACE_RE = re.compile(r"\s+")


def normalize(items: list[str]) -> list[str]:
    # co-21: O(n), but each call does a regex substitution -- a real per-item cost.
    return [_WHITESPACE_RE.sub(" ", item.strip()) for item in items]


def dedupe_naive(items: list[str]) -> list[str]:
    # co-21: O(n^2) -- `in` on a growing list re-scans it every time.
    seen: list[str] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def process(items: list[str]) -> list[str]:
    normalized = normalize(items)
    return dedupe_naive(normalized)


def make_items(n: int) -> list[str]:
    return [f"  item-{i % (n // 10 + 1)}  extra   spacing  " for i in range(n)]
