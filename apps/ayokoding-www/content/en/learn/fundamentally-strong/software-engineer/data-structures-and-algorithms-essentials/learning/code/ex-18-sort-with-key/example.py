"""Example 18: sorted() with a key Function."""

# key=len computes a sort key for EACH element once, then sorts by that key (co-15).
words: list[str] = ["banana", "fig", "kiwi", "watermelon"]  # => varying lengths
by_length = sorted(words, key=len)  # => sorts by len(word), not alphabetically
print(by_length)  # => Output: ['fig', 'kiwi', 'banana', 'watermelon']

assert by_length == ["fig", "kiwi", "banana", "watermelon"]  # => confirms length order
assert [len(w) for w in by_length] == [3, 4, 6, 10]  # => confirms lengths are ascending
print("ex-18 OK")  # => Output: ex-18 OK
