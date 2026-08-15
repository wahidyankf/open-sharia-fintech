server = {"tools": ["weather"], "resources": ["policy"]}  # => MCP-like contract fixture
assert server["tools"] and server["resources"]  # => server exposes both surfaces
print("PASS: mcp-server")  # => offline acceptance result
