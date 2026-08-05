"""Report invalid input and use a non-zero process status."""

import sys

print("notes: title must not be empty", file=sys.stderr)
raise SystemExit(2)
