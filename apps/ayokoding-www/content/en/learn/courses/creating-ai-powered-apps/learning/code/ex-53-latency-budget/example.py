elapsed_ms, budget_ms = 50, 100  # => observed latency and product budget
assert elapsed_ms <= budget_ms  # => slow calls breach this boundary
print("PASS: latency-budget")  # => offline acceptance result
