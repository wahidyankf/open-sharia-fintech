examples = {"yes": "true", "no": "false"}  # => few-shot format fixture
reply = examples["yes"]  # => mock follows the demonstrated pattern
assert reply == "true"  # => output conforms to example format
print("PASS: few-shot")  # => offline acceptance result
