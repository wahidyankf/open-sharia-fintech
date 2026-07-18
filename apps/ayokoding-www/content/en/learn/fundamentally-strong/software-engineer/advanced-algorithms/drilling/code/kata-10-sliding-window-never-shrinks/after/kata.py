"""Kata 10 (after): on a duplicate, the window's left edge advances past the PREVIOUS occurrence -- it genuinely shrinks."""


def longest_unique_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = (
                last_seen[ch] + 1
            )  # => SHRINK: jump the left edge past the earlier occurrence of `ch`
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


print(longest_unique_substring("abcabcbb"))
print(longest_unique_substring("abcabcbb") == 3)
