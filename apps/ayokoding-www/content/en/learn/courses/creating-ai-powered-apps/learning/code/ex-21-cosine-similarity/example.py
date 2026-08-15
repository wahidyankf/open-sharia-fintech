from math import sqrt

left, right = (1.0, 0.0), (1.0, 0.0)  # => identical semantic-vector fixture
score = sum(a * b for a, b in zip(left, right)) / (
    sqrt(sum(a * a for a in left)) * sqrt(sum(b * b for b in right))
)
assert score == 1.0  # => identical directions have maximum cosine similarity
print("PASS: cosine-similarity")  # => offline acceptance result
