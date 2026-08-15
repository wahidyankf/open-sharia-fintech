from typing import Final  # => typed local tokenizer approximation

TOKENS: Final[int] = len("one two three".split())  # => deterministic message count
assert TOKENS == 3
print("PASS: count-tokens")  # => known-value check
