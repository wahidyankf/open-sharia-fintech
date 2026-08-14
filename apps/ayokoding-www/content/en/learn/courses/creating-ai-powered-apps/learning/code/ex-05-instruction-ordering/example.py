prompt = ("instruction", "context", "input")  # => explicit safe ordering
assert prompt[0] == "instruction" and prompt[-1] == "input"  # => boundary is stable
print("PASS: instruction-ordering")  # => offline acceptance result
