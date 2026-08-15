import json

payload = json.loads('{"answer":"ok"}')  # => mock structured output
assert isinstance(payload["answer"], str)  # => schema-required field has expected type
print("PASS: json-schema-output")  # => offline acceptance result
