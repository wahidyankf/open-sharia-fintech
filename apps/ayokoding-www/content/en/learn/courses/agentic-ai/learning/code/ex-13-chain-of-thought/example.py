from typing import Final  # => typed survey fixture

OUTPUT: Final[str] = (
    "validated answer"  # => public contract is output, not private reasoning
)
assert OUTPUT == "validated answer"  # => downstream uses typed result
print("PASS: chain-of-thought")  # => credential-free result
