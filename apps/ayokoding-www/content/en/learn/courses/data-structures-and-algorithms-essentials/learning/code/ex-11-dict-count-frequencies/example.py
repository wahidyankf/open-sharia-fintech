"""Example 11: Count Character Frequencies with a Dict."""


# Builds a char -> count frequency map with one O(n) pass (co-08).
def count_chars(text: str) -> dict[str, int]:  # => a plain function, no class needed
    counts: dict[str, int] = {}  # => starts empty
    for char in text:  # => visits each character once, O(n) total
        counts[char] = counts.get(char, 0) + 1  # => .get(char, 0) avoids a KeyError
        # => on a new char this inserts 1; on a repeat it increments the existing count
    return counts  # => the finished char -> count map


frequencies = count_chars("banana")  # => tallies b, a, n, a, n, a
print(frequencies)  # => Output: {'b': 1, 'a': 3, 'n': 2}

assert frequencies == {"b": 1, "a": 3, "n": 2}  # => confirms every count matches
assert sum(frequencies.values()) == len("banana")  # => confirms counts sum to length
print("ex-11 OK")  # => Output: ex-11 OK
