from typing import Final  # => typed store fixture

STORE: Final[dict[str, tuple[float, ...]]] = {
    "doc": (1.0,)
}  # => indexed document vector
assert "doc" in STORE
print("PASS: build-a-vector-store")  # => queryable index
