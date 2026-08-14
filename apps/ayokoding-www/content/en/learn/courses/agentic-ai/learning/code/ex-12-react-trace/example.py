from typing import Final  # => typed survey fixture

TRACE: Final[tuple[str, str]] = ("decide", "call_tool")  # => decision precedes action
assert TRACE[0] == "decide"  # => trace records behavior, not private thought
print("PASS: react-trace")  # => credential-free result
