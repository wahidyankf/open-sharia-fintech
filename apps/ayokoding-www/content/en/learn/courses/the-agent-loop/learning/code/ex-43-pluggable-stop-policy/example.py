from typing import Final  # => typed policy fixture

POLICY: Final[str] = "max_turns"  # => injected stop behavior
assert POLICY == "max_turns"
print("PASS: pluggable-stop-policy")  # => swapped policy
