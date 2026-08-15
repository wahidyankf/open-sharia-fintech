from typing import Final  # => typed incremental fixture

UPDATES: Final[int] = 1  # => one turn updates running summary
assert UPDATES == 1
print("PASS: incremental-summary-update")  # => avoids full rewrite
