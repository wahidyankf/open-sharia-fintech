from typing import Final  # => typed survey fixture

SCOPE: Final[str] = "sandbox"  # => execution containment label
assert SCOPE == "sandbox"  # => host authority is not granted
print("PASS: tool-sandbox")  # => offline result
