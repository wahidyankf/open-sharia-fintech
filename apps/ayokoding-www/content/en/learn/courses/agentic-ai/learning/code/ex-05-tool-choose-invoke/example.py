from typing import Final  # => typed survey fixture

CHOICE: Final[str] = "lookup"  # => model proposal represented as data
assert CHOICE in {"lookup", "search"}  # => application allowlist governs choice
print("PASS: tool-choose-invoke")  # => credential-free result
