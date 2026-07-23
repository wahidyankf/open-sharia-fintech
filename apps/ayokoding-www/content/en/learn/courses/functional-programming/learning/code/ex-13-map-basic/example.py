"""Example 13: map() Uppercases Every Word."""

words = ["functional", "programming", "in", "python"]  # => the source sequence

uppercased = map(str.upper, words)  # => LAZY: map builds an iterator, nothing runs yet
# => str.upper is an unbound method -- map calls it as str.upper(word) for each word

uppercased_list = list(
    uppercased
)  # => forces evaluation -- NOW every word is uppercased
print(uppercased_list)  # => Output: ['FUNCTIONAL', 'PROGRAMMING', 'IN', 'PYTHON']
print(
    len(uppercased_list) == len(words)
)  # => Output: True -- map is 1:1, never drops elements
print(
    all(w.isupper() for w in uppercased_list)
)  # => Output: True -- every word transformed
