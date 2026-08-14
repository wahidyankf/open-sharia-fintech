corpus = ["facts", "ignore instructions"]  # => hostile corpus regression fixture
safe = [
    item for item in corpus if "ignore instructions" not in item
]  # => retrieval filter
assert safe == ["facts"]  # => injected item is not passed as authority
print("PASS: injection-corpus-test")  # => offline acceptance result
