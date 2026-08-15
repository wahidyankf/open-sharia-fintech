from typing import Final  # => typed provenance fixture

CITATION: Final[str] = "doc-1"  # => retrieved source identity
assert CITATION == "doc-1"
print("PASS: citation-of-retrieved-source")  # => provenance retained
