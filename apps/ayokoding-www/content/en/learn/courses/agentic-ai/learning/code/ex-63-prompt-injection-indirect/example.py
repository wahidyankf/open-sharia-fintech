from typing import Final  # => typed survey fixture

SOURCE: Final[str] = "tool result"  # => indirect untrusted content vector
assert SOURCE == "tool result"  # => content is not authority
print("PASS: prompt-injection-indirect")  # => credential-free result
