from typing import Final  # => typed offline loop state

STATES: Final[tuple[str, str]] = ("tool", "final")  # => model-tool-model path
assert STATES[-1] == "final"
print("PASS: loop-until-final")  # => stop reached
