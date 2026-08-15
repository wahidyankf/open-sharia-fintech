dense, sparse = {"a"}, {"b"}  # => independent retrieval channels
assert dense | sparse == {"a", "b"}  # => hybrid retrieval contributes both
print("PASS: hybrid-dense-sparse")  # => offline acceptance result
