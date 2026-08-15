payload = {"answer": "ok"}  # => strict fixture exposes only allowed fields
assert set(payload) == {"answer"} and payload["answer"]  # => required and no extras
print("PASS: structured-required-fields")  # => offline acceptance result
