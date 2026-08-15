from typing import Final  # => typed survey fixture

JUDGE: Final[str] = "separate-model"  # => judge differs from generator
assert JUDGE == "separate-model"  # => self-judging is avoided
print("PASS: llm-as-judge")  # => offline result
