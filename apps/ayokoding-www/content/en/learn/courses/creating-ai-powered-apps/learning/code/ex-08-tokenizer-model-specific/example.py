counts = {"model-a": 3, "model-b": 4}  # => tokenizers need not agree
assert counts["model-a"] != counts["model-b"]  # => count is model specific
print("PASS: tokenizer-model-specific")  # => offline acceptance result
