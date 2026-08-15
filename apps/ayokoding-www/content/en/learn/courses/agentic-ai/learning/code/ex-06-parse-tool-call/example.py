from typing import Final  # => typed survey fixture

CALL: Final[dict[str, str]] = {
    "name": "lookup",
    "query": "policy",
}  # => parsed call data
assert CALL["query"] == "policy"  # => dispatch happens only after parsing
print("PASS: parse-tool-call")  # => credential-free result
