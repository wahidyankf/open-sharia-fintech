context = "The policy says validate JSON."  # => retrieved local evidence
answer = "Validate JSON."  # => mock generation grounded in context
assert "validate json" in context.lower() and answer  # => retrieve then answer
print("PASS: rag-retrieve-augment-generate")  # => offline acceptance result
