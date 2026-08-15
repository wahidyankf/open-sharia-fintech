tool = {"name": "weather", "input_schema": {"city": "string"}}  # => typed offered tool
assert tool["name"] == "weather"  # => client can expose the contract
print("PASS: tool-definition")  # => offline acceptance result
