from typing import Final  # => typed survey fixture

STEP: Final[str] = "lookup"  # => one authorized action
assert STEP == "lookup"  # => execution unit remains small
print("PASS: executor-step")  # => credential-free result
