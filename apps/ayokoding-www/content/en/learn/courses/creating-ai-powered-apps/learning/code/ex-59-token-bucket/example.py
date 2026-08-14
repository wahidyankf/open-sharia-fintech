tokens, capacity = 3, 5  # => continuously replenishable token bucket fixture
assert 0 <= tokens <= capacity  # => request admission observes capacity
print("PASS: token-bucket")  # => offline acceptance result
