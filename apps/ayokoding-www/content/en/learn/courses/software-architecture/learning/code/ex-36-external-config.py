"""Worked Example 36: validate a deployment-provided configuration value."""

import os

timeout_seconds = int(os.environ.get("PAYMENT_TIMEOUT_SECONDS", "30"))
assert timeout_seconds > 0
print(timeout_seconds)
