output = {"answer": "ok"}  # => candidate model output
assert set(output) == {"answer"}  # => unknown fields are rejected
print("PASS: output-validation")  # => offline acceptance result
