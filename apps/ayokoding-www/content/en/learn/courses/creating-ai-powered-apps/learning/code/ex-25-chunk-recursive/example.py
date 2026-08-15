text = "first paragraph\n\nsecond paragraph"  # => natural-separator fixture
chunks = text.split("\n\n")  # => recursive splitter prefers paragraph boundary
assert chunks == [
    "first paragraph",
    "second paragraph",
]  # => semantic units stay intact
print("PASS: chunk-recursive")  # => offline acceptance result
