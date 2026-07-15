"""Example 12 (v1): Print-Debugging a One-Off Script -- WITH the diagnostic prints still in."""

from __future__ import annotations


def calculate_average(scores: list[float]) -> float:
    total = sum(scores)
    print(f"DEBUG total={total}")  # diagnostic print #1
    count = len(scores) - 1  # seeded bug: should be len(scores), no "-1"
    print(f"DEBUG count={count}")  # diagnostic print #2
    return total / count


if __name__ == "__main__":
    print(calculate_average([10.0, 20.0, 30.0, 40.0]))
