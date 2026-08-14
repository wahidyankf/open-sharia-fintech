from typing import Final  # => typed survey fixture

RISK: Final[str] = "excessive agency"  # => OWASP category label
assert RISK.startswith("excessive")  # => authority is identified as risk
print("PASS: excessive-agency")  # => credential-free result
