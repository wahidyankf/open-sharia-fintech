from typing import Final  # => typed strategy fixture

CHOICE: Final[str] = "retrieval"  # => local corpus policy result
assert CHOICE == "retrieval"
print("PASS: retrieval-vs-stuffing")  # => strategy explicit
