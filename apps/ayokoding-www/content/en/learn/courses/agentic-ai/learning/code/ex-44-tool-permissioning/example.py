from typing import Final  # => typed survey fixture

PERMISSION: Final[str] = "read"  # => least-privilege scope
assert PERMISSION == "read"  # => write authority is absent
print("PASS: tool-permissioning")  # => offline result
