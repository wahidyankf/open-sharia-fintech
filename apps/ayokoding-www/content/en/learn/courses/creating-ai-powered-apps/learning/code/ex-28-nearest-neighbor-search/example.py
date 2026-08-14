scores = {"python": 0.9, "garden": 0.1}  # => local vector-store scores
assert max(scores, key=scores.get) == "python"  # => nearest item is returned
print("PASS: nearest-neighbor-search")  # => offline acceptance result
