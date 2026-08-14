chunk = "API guide"  # => original local chunk
contextual = (
    "Document: engineering handbook. " + chunk
)  # => context prefix enriches embedding text
assert chunk in contextual  # => original evidence is preserved
print("PASS: contextual-retrieval")  # => offline acceptance result
