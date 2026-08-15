deltas = ["hel", "lo"]  # => deterministic SSE-like chunks
assert "".join(deltas) == "hello"  # => UI may assemble incremental content
print("PASS: streaming-deltas")  # => offline acceptance result
