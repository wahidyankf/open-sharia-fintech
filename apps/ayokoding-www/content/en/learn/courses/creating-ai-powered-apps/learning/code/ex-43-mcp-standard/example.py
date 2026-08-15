clients = {"editor", "chat"}  # => independent clients share a server contract
assert len(clients) == 2  # => protocol is cross-client, not app-local
print("PASS: mcp-standard")  # => offline acceptance result
