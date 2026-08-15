from typing import Final  # => typed truncation fixture

TEXT: Final[str] = "result... [truncated]"  # => provenance remains in context
assert TEXT.endswith("[truncated]")
print("PASS: truncate-tool-results")  # => truncation noted
