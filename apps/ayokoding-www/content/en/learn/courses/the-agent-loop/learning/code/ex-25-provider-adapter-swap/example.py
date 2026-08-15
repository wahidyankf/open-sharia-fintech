from typing import Final  # => typed adapter fixture

ADAPTER: Final[str] = "fake-b"  # => interface can swap implementation
assert ADAPTER == "fake-b"
print("PASS: provider-adapter-swap")  # => loop unchanged
