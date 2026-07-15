"""Example 35: Line-Level vs. Function-Level Attribution -- the SAME function, profiled two ways."""

from __future__ import annotations


@profile  # noqa: F821 -- kernprof injects this name into builtins
def build_merged_report(a: list[int], b: list[int]) -> list[int]:
    merged: list[int] = []
    for x in a:
        merged.append(x)  # cheap
    for y in b:
        merged.append(y)  # cheap
    merged = sorted(set(merged))  # cheap, ONE call
    lookup: list[int] = []
    for item in merged:
        if (
            item in merged
        ):  # seeded bug: O(n) `in` on a LIST, called once per item -- O(n^2) overall
            lookup.append(item)
    return lookup


if __name__ == "__main__":
    print(len(build_merged_report(list(range(3000)), list(range(1500, 4500)))))
