from typing import Final  # => typed prefix-reuse fixture

STABLE: Final[str] = "system|tools|corpus"  # => reusable portion
bad_a: str = "time=10|" + STABLE
bad_b: str = "time=11|" + STABLE  # => volatile prefix destroys reuse
good_a: str = STABLE + "|time=10"
good_b: str = STABLE + "|time=11"  # => volatile tail restores reuse
assert (
    bad_a.split("|", 1)[0] != bad_b.split("|", 1)[0]
    and good_a.split("|", 3)[:3] == good_b.split("|", 3)[:3]
)
print(
    "PASS: one-volatile-field-destroys-the-prefix"
)  # => cache mechanism, distinct from accuracy
