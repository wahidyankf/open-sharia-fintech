"""Example 77: Longest Substring Without Repeating Characters."""


# Grows a window while characters stay unique; shrinks from the left on a repeat --
# a set tracks the window's current contents for O(1) membership checks (co-20, co-09).
def longest_unique_substring(text: str) -> int:  # => a sliding-window function
    seen: set[str] = set()  # => the DISTINCT characters currently inside the window
    left = 0  # => the window's left edge (inclusive)
    best = 0  # => the longest window length found so far
    for right, char in enumerate(
        text
    ):  # => the window's right edge advances every step
        while char in seen:  # => shrink from the left UNTIL the duplicate is expelled
            seen.remove(text[left])  # => removes the leftmost character from the window
            left += 1  # => shrinks the window by one from the left
        seen.add(
            char
        )  # => the window is now duplicate-free again -- admit the new char
        best = max(best, right - left + 1)  # => window length is right - left + 1
    return best  # => the longest duplicate-free window seen across the whole string


length = longest_unique_substring(
    "abcabcbb"
)  # => longest unique run is "abc", length 3
print(length)  # => Output: 3

assert (
    length == 3
)  # => confirms "abc" (or any of its repeats) is the longest unique run
assert (
    longest_unique_substring("") == 0
)  # => confirms the empty-string edge case is handled
print("ex-77 OK")  # => Output: ex-77 OK
