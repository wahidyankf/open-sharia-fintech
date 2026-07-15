"""Example 34: Line Profiling with @profile and kernprof."""

from __future__ import annotations


@profile  # noqa: F821 -- kernprof injects this name into builtins; only valid when run via kernprof
def build_sorted_report(rows: list[int]) -> list[int]:
    seen: list[int] = []
    for r in rows:
        seen.append(r)
        seen.sort()  # seeded bug: re-sorts the WHOLE list on every single append -- O(n^2 log n)
    return seen


if __name__ == "__main__":
    print(len(build_sorted_report(list(range(2000, 0, -1)))))
