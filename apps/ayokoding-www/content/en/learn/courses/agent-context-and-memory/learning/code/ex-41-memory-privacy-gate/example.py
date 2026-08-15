from typing import Final  # => typed privacy fixture

CANDIDATES: Final[tuple[str, ...]] = (
    "prefers concise answers",
    "api_key=secret",
)  # => proposed writes
safe: tuple[str, ...] = tuple(
    item for item in CANDIDATES if "secret" not in item
)  # => reject sensitive data
assert safe == ("prefers concise answers",)
print("PASS: memory-privacy-gate")  # => secret blocked
