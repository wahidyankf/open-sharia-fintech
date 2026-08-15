left, right = (0.6, 0.8), (0.6, 0.8)  # => pre-normalized vector fixture
assert (
    sum(a * b for a, b in zip(left, right)) == 1.0
)  # => dot equals cosine when normalized
print("PASS: normalized-dot-product")  # => offline acceptance result
