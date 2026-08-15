from typing import Final  # => typed survey fixture

CASE: Final[dict[str, str]] = {"input": "task", "expected": "done"}  # => dataset record
assert CASE["expected"] == "done"  # => deep eval design is forward-linked
print("PASS: eval-dataset")  # => credential-free result
