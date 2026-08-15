from typing import Final  # => typed personalization fixture

MEMORY: Final[dict[str, str]] = {"format": "bullet list"}  # => recalled preference
result: str = f"Plan in {MEMORY['format']}"  # => personalized task response
assert result == "Plan in bullet list"
print("PASS: memory-backed-agent-task")  # => memory changes outcome
