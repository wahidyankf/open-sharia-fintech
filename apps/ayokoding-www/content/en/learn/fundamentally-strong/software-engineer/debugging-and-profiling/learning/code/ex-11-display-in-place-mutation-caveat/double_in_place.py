"""Example 11: The display In-Place-Mutation Caveat."""

from __future__ import annotations


def double_in_place(lst: list[int]) -> list[int]:
    for i in range(len(lst)):
        lst[i] = (
            lst[i] * 2
        )  # mutates the SAME list object -- no rebinding of the name 'lst'
    return lst


if __name__ == "__main__":
    print(double_in_place([1, 2, 3]))
