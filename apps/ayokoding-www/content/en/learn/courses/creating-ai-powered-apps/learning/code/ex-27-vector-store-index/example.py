index = {"python": (1.0, 0.0), "garden": (0.0, 1.0)}  # => in-memory vector-store mock
query = (1.0, 0.0)  # => query embedding
best = max(
    index, key=lambda key: sum(a * b for a, b in zip(index[key], query))
)  # => top-k search primitive
assert best == "python"  # => indexed nearest item is queryable
print("PASS: vector-store-index")  # => offline acceptance result
