"""Example 78: Counter Frequency."""

from collections import Counter  # => imports the specialized dict-subclass for tallying

# Counter counts every hashable element's occurrences in one linear pass.
words: list[str] = ["ada", "grace", "ada", "alan", "ada", "grace"]
# => words has 6 entries; "ada" repeats 3 times, "grace" repeats twice
counts = Counter(words)  # => tallies every element's frequency in one pass
top_word, top_count = counts.most_common(1)[0]  # => the single top (word, count) pair
print(top_word, top_count)  # => "ada" appears 3 times -- Output: ada 3
