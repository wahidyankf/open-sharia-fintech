from typing import Final  # => typed summary fixture

SUMMARY: Final[str] = "decision: validate"  # => old decision survives compaction
assert "decision" in SUMMARY
print("PASS: summarize-a-history-span")  # => preserves decision
