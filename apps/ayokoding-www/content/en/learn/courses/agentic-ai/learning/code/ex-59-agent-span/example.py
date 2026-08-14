from typing import Final  # => typed survey fixture

SPAN: Final[str] = "invoke_agent"  # => observable operation name
assert SPAN == "invoke_agent"  # => trace ownership is forward-linked
print("PASS: agent-span")  # => credential-free result
