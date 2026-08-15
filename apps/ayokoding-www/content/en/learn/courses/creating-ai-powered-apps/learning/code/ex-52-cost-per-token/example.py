tokens, price = 1000, 0.000001  # => local unit-cost fixture
assert tokens * price == 0.001  # => cost math is explicit
print("PASS: cost-per-token")  # => offline acceptance result
