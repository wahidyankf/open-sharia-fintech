tokens = len("count these tokens".split())  # => deterministic local token approximation
assert tokens == 3  # => budgeting sees a concrete count
print("PASS: token-count")  # => offline acceptance result
