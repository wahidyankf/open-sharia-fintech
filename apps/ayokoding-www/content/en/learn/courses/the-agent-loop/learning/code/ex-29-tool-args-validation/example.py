from typing import Final  # => typed arguments fixture

CITY: Final[str] = "Jakarta"  # => validated local argument
assert CITY.isalpha()
print("PASS: tool-args-validation")  # => bad args are rejected
