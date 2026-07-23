"""Kata 10 (before): the window only grows -- the left edge never advances past a duplicate, so it over-counts."""


def longest_unique_substring(s: str) -> int:
    seen: set[str] = set()
    left = 0
    best = 0
    for right in range(len(s)):
        if s[right] in seen:
            pass  # BUG: detects the duplicate but never moves `left` forward or evicts anything from `seen`
        seen.add(s[right])
        best = max(best, right - left + 1)
    return best


print(longest_unique_substring("abcabcbb"))
print(
    longest_unique_substring("abcabcbb") == 3
)  # true answer is 3 ("abc") -- the window must SHRINK on a repeat
