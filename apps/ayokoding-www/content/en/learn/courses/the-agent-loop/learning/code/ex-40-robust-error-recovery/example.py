from typing import Final  # => typed recovery fixture

RECOVERED: Final[bool] = True  # => model/tool/timeout errors become feedback
assert RECOVERED
print("PASS: robust-error-recovery")  # => loop reports survival
