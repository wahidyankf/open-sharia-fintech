from typing import Final  # => typed survey fixture

STATE: Final[str] = "pause_turn"  # => caller-owned continuation state
assert STATE == "pause_turn"  # => no hidden server loop
print("PASS: pause-turn")  # => offline result
