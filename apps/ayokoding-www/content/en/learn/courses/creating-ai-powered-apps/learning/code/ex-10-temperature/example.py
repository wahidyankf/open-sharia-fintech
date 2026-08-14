temperature = 0.7  # => diversity control in an application request
assert 0.0 <= temperature <= 1.0  # => fixture stays within its chosen policy
print("PASS: temperature")  # => offline acceptance result
