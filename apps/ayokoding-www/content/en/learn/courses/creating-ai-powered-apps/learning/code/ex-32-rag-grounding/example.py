sources = {"policy-1"}  # => permitted retrieved evidence
assert "policy-1" in sources  # => answer may only cite retrieved context
print("PASS: rag-grounding")  # => offline acceptance result
