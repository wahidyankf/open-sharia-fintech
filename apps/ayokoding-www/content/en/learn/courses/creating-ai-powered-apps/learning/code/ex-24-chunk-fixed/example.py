text, size, overlap = "abcdefgh", 4, 1  # => fixed chunk configuration
chunks = [
    text[index : index + size] for index in range(0, len(text), size - overlap)
]  # => retain boundary overlap
assert chunks[0] == "abcd" and chunks[1].startswith(
    "d"
)  # => overlap preserves boundary text
print("PASS: chunk-fixed")  # => offline acceptance result
