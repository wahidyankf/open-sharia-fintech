"""Example 72: Minimum Window Substring Covering a Target Character Set."""

# Another variable-size window (co-26): grow the right edge until the window
# covers every needed character, then shrink the LEFT edge as far as
# possible while STILL covering it -- recording the smallest window along
# the way. A `need` counter tracks exactly how many more characters are missing.
from collections import Counter  # => a dict subclass that tracks per-character counts


def min_window_substring(s: str, target: str) -> str:  # => O(len(s) + len(target))
    if not target or not s:  # => an empty target or source has no valid window
        return ""  # => nothing to search for, or nothing to search in
    need = Counter(target)  # => char -> how many of it the window still needs
    missing = len(target)  # => total count of characters still unsatisfied
    left = 0  # => the window's left edge
    best_left, best_len = 0, float("inf")  # => tracks the best window found so far
    for right, ch in enumerate(s):  # => grows the window's right edge
        if need[ch] > 0:  # => this character is still needed somewhere in the window
            missing -= 1  # => one fewer character left to satisfy
        need[ch] -= (  # => opens the need-counter decrement
            1  # => consumes one unit of "need" for this character (may go negative)
        )  # => closes the decrement assignment
        while missing == 0:  # => the window FULLY covers target -- try to SHRINK it
            if (  # => opens the new-best-window check
                right - left + 1  # => this window's own current length
                < best_len  # => this window's length beats the current best
            ):  # => this window beats the best found so far
                best_left, best_len = left, right - left + 1  # => records the new best
            need[s[left]] += 1  # => giving back the leftmost character's "need" slot
            if need[s[left]] > 0:  # => that character is now missing again
                missing += 1  # => the window no longer fully covers target
            left += 1  # => shrinks the window by advancing the left edge
    return (  # => opens the found-window-or-empty-string result
        "" if best_len == float("inf") else s[best_left : best_left + int(best_len)]
    )  # => final window


print(min_window_substring("ADOBECODEBANC", "ABC"))  # => Output: BANC
print(min_window_substring("a", "a"))  # => Output: a
print(min_window_substring("a", "aa"))  # => Output: (empty) -- "aa" is never coverable

assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"  # => the classic answer
assert min_window_substring("a", "a") == "a"  # => the trivial single-character case
assert min_window_substring("a", "aa") == ""  # => confirms an impossible target
for ch in "ABC":  # => confirms the found window genuinely contains every needed char
    assert ch in min_window_substring(  # => opens the per-character containment check
        "ADOBECODEBANC", "ABC"
    )  # => this required character is present somewhere in the found window
print("ex-72 OK")  # => Output: ex-72 OK
