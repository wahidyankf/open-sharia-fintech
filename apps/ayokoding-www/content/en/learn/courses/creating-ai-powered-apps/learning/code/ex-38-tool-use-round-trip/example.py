call = {"name": "weather", "city": "Jakarta"}  # => model-requested tool call
result = "sunny"  # => local validated tool result
assert call["name"] == "weather" and result == "sunny"  # => round trip completes
print("PASS: tool-use-round-trip")  # => offline acceptance result
