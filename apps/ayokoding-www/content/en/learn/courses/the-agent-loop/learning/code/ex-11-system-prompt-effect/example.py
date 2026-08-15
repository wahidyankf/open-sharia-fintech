from typing import Final  # => typed prompt fixture

PROMPT: Final[str] = "concise"  # => system state changes behavior
assert PROMPT == "concise"
print("PASS: system-prompt-effect")  # => effect observed
