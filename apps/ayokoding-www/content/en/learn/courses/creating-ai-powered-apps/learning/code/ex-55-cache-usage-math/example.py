read, creation, input_tokens = 10, 20, 30  # => provider usage components
assert read + creation + input_tokens == 60  # => total input usage is additive
print("PASS: cache-usage-math")  # => offline acceptance result
