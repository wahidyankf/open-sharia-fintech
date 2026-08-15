from typing import Final  # => typed survey fixture

OWNERS: Final[dict[str, str]] = {"ui": "client", "database": "server"}  # => trust zones
assert OWNERS["database"] == "server"  # => execution location is explicit
print("PASS: client-vs-server-tools")  # => credential-free result
