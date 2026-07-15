"""Example 12 (v2): Print-Debugging a One-Off Script -- the FIX, with the prints removed again."""

from __future__ import annotations


def calculate_average(scores: list[float]) -> float:
    total = sum(scores)
    count = len(scores)  # fixed: no more spurious "-1"
    return total / count


if __name__ == "__main__":
    print(calculate_average([10.0, 20.0, 30.0, 40.0]))
