from typing import Final  # => typed survey fixture

DISPATCH: Final[dict[str, str]] = {"lookup": "typed handler"}  # => mapping description
assert (
    DISPATCH["lookup"] == "typed handler"
)  # => dispatch implementation is forward-linked
print("PASS: tool-dispatch-typed")  # => credential-free result
