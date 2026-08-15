tool_result = {"city": "Jakarta"}  # => forced tool returns typed object shape
assert tool_result["city"].isalpha()  # => caller validates the forced result
print("PASS: tool-for-structured")  # => offline acceptance result
