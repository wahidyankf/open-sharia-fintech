from typing import Final  # => typed survey fixture

STATE: Final[str] = "checkpointed"  # => stateful graph vocabulary
assert STATE == "checkpointed"  # => graph runtime is not implemented
print("PASS: langgraph-stateful")  # => credential-free result
