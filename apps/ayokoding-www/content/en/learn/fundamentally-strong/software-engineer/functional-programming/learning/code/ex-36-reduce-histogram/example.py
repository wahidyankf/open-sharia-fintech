"""Example 36: Building a Histogram with reduce."""

from functools import reduce  # => reduce folds words into the histogram below


def add_to_histogram(  # => the "how to fold one more element in" step
    histogram: dict[str, int],
    word: str,  # => the accumulator and the next element, reduce's own calling convention
) -> dict[str, int]:  # => closes the multi-line signature above
    histogram[word] = (
        histogram.get(word, 0) + 1
    )  # => increments, defaulting missing keys to 0
    return histogram  # => reduce expects the combiner to return the NEW accumulator


words = ["a", "b", "a", "c", "b", "a"]  # => the source sequence being counted

histogram = reduce(
    add_to_histogram, words, {}
)  # => folds words into ONE dict, seeded empty

# => reduce is the general-purpose fold every other aggregation specializes
print(histogram)  # => Output: {'a': 3, 'b': 2, 'c': 1}
print(histogram["a"])  # => Output: 3 -- 'a' appeared three times
print(
    sum(histogram.values()) == len(words)
)  # => Output: True -- every word counted exactly once
