"""Example 29: Four Ways -- Imperative."""


def word_frequency_imperative(text: str) -> dict[str, int]:  # => way #1 of 4: loop + dict, mutated in place
    counts: dict[str, int] = {}  # => mutable accumulator
    for word in text.split():  # => explicit iteration
        counts[word] = counts.get(word, 0) + 1  # => explicit mutation, one word at a time
    return counts  # => the final mutated state


sample = "red blue red green blue red"  # => shared sample text for all four "four-ways" examples
result = word_frequency_imperative(sample)  # => run it
print(result)  # => red: 3, blue: 2, green: 1
# => Output: {'red': 3, 'blue': 2, 'green': 1}
