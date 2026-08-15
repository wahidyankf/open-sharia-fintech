from typing import Final  # => typed trace fixture

EVENTS: Final[tuple[str, str]] = ("turn", "summary")  # => complete observable run
assert EVENTS[-1] == "summary"
print("PASS: observable-agent-run")  # => inspectable trace
