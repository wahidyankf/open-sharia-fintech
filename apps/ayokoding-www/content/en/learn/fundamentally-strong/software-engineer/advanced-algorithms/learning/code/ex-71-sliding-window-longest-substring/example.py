"""Example 71: Longest Substring Without Repeating Characters -- Variable Window."""

# A VARIABLE-size sliding window (co-26): grow the right edge always; shrink
# the LEFT edge only when a repeat is detected, using a dict of last-seen
# positions to jump the left edge directly past the repeat -- O(n), not O(n^2).


def longest_unique_substring_length(s: str) -> int:  # => O(n): one pass, amortized
    last_seen: dict[str, int] = {}  # => char -> the most recent index it was seen at
    left = 0  # => the window's left edge (inclusive)
    best = 0  # => the longest window length found so far
    for right, ch in enumerate(  # => opens the right-edge growth loop
        s  # => the string being scanned
    ):  # => grows the window's right edge one char at a time
        if ch in last_seen and last_seen[ch] >= left:  # => a repeat WITHIN the window
            left = (  # => opens the left-edge jump
                last_seen[ch] + 1
            )  # => jumps left past the earlier occurrence directly
        last_seen[ch] = right  # => records this character's newest position
        best = max(best, right - left + 1)  # => updates the longest window seen so far
    return best  # => the length of the longest substring with no repeated characters


def brute_force_longest_unique_substring(s: str) -> int:  # => O(n^2): every start point
    best = 0  # => the longest repeat-free run found so far
    for i in range(len(s)):  # => tries every possible starting index
        seen: set[str] = set()  # => characters seen in the current run from i
        for j in range(i, len(s)):  # => extends as far as possible without a repeat
            if s[j] in seen:  # => this character already appeared in the current run
                break  # => a repeat -- this run from i stops here
            seen.add(s[j])  # => records this character as seen in the current run
            best = max(best, j - i + 1)  # => updates the longest run found
    return best  # => ground truth, for comparison


test_strings: list[str] = [  # => opens the varied-test-case list
    "abcabcbb",  # => a mix with a repeating 3-char block
    "bbbbb",  # => every character is the same, worst case for repeats
    "pwwkew",  # => a repeat right at the start
    "",  # => the empty-string edge case
    "abcdef",  # => no repeats at all -- the whole string is the answer
]  # => varied test cases
for s in test_strings:  # => checks the fast approach against brute force, per string
    fast = longest_unique_substring_length(s)  # => O(n) result
    brute = brute_force_longest_unique_substring(s)  # => O(n^2) ground truth
    print(f"{s!r}: {fast}")  # => Output: one "'string': length" line per test string
    assert fast == brute  # => confirms both approaches agree exactly

assert longest_unique_substring_length("abcabcbb") == 3  # => "abc"
assert longest_unique_substring_length("bbbbb") == 1  # => "b" -- all repeats
assert longest_unique_substring_length("pwwkew") == 3  # => "wke"
print("ex-71 OK")  # => Output: ex-71 OK
