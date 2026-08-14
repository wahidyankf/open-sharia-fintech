from typing import Final  # => typed survey fixture

RESULTS: Final[tuple[str, str]] = ("fact", "draft")  # => worker outputs
assert "fact" in RESULTS  # => synthesis input is explicit data
print("PASS: orchestrator-synthesize")  # => offline result
