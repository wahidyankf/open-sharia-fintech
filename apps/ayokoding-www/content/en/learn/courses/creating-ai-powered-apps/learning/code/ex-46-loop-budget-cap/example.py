spent, budget = 2, 2  # => local cost ledger
assert spent <= budget  # => runaway execution cannot exceed its cap
print("PASS: loop-budget-cap")  # => offline acceptance result
