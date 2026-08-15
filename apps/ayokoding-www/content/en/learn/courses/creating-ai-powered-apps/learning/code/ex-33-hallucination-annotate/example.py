claim, evidence = "made up", set()  # => unsupported generation fixture
assert claim not in evidence  # => unsupported text is identified, not trusted
print("PASS: hallucination-annotate")  # => offline acceptance result
