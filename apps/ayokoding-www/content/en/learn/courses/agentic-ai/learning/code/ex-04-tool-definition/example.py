from typing import Final  # => typed survey fixture

TOOL: Final[dict[str, str]] = {
    "name": "lookup",
    "schema": "query:str",
}  # => tool contract
assert TOOL["name"] == "lookup"  # => schema is offered, not executed
print("PASS: tool-definition")  # => credential-free result
