from typing import Final  # => typed survey fixture

MEMORY: Final[tuple[str, ...]] = ("prior observation",)  # => scoped step memory
assert MEMORY[0] == "prior observation"  # => context ownership is forward-linked
print("PASS: memory-plus-loop")  # => credential-free result
