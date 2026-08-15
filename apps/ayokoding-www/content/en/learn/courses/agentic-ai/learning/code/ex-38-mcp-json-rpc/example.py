from typing import Final  # => typed survey fixture

TRANSPORT: Final[str] = "JSON-RPC 2.0"  # => protocol label
assert TRANSPORT.endswith("2.0")  # => transport is explicit
print("PASS: mcp-json-rpc")  # => offline result
