import json

invalid = "not json"  # => untrusted model text
try:
    json.loads(invalid)  # => parser rejects invalid syntax
except json.JSONDecodeError:
    print("PASS: parse-validate-output")  # => rejection is expected acceptance behavior
else:
    raise AssertionError("invalid output was accepted")
