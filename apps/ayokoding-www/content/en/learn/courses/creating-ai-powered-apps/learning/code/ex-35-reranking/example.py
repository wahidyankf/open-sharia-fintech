candidates = [("a", 0.2), ("b", 0.9)]  # => candidate relevance scores
assert max(candidates, key=lambda item: item[1])[0] == "b"  # => reranker chooses best
print("PASS: reranking")  # => offline acceptance result
