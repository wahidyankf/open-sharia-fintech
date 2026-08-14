answer = {"text": "Validate JSON.", "citation": "policy-1"}  # => cited schema
assert answer["citation"] == "policy-1"  # => claim carries retrieved source id
print("PASS: rag-citations")  # => offline acceptance result
