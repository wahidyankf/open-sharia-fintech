"""Keep machine-readable output separate from diagnostics."""

import sys

print("pending=2")
print("notes: status served locally", file=sys.stderr)
