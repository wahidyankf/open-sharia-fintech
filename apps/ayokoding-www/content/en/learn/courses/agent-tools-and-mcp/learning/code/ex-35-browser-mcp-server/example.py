# A local browser shape avoids live automation.
tools: dict[str, str] = {"navigate": "fixture navigation"}
# Discovery exposes only the bounded capability.
assert "navigate" in tools
# Print the advertised tool.
print(tools)
