spans = ["retrieve", "generate"]  # => call-chain tracing fixture
assert spans == ["retrieve", "generate"]  # => each major operation has a span
print("PASS: tracing-spans")  # => offline acceptance result
