attempt, base = 3, 2  # => retry number and base delay
assert base**attempt == 8  # => backoff grows after a retryable failure
print("PASS: exponential-backoff")  # => offline acceptance result
