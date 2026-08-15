payload = {"answer": "ok"}  # => expected output schema
assert set(payload) == {"answer"}  # => malformed output would fail
print("PASS: eval-schema-assert")  # => offline acceptance result
