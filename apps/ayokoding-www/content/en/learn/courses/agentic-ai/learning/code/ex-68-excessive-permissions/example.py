from typing import Final  # => typed survey fixture

SCOPE: Final[str] = "read"  # => least-privilege permission
assert SCOPE == "read"  # => write authority is not granted
print("PASS: excessive-permissions")  # => credential-free result
