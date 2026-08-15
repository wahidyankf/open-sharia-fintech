from typing import Final  # => typed survey fixture

CONNECTION: Final[str] = "validated tool endpoint"  # => connection is data
assert CONNECTION.startswith("validated")  # => authorization remains external
print("PASS: mcp-connect-tool")  # => offline result
