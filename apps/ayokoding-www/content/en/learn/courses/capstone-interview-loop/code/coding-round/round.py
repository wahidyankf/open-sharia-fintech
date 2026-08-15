"""Small reference solves for the timed interview-loop coding round."""

from collections.abc import Sequence


def pair_indices(numbers: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return indices of the first pair whose values add to target, if one exists."""
    seen: dict[int, int] = {}
    for index, value in enumerate(numbers):
        complement = target - value
        if complement in seen:
            return (seen[complement], index)
        seen[value] = index
    return None


def longest_unique_run(text: str) -> int:
    """Return the length of the longest contiguous substring with unique characters."""
    start = 0
    longest = 0
    last_seen: dict[str, int] = {}
    for end, character in enumerate(text):
        if character in last_seen and last_seen[character] >= start:
            start = last_seen[character] + 1
        last_seen[character] = end
        longest = max(longest, end - start + 1)
    return longest
