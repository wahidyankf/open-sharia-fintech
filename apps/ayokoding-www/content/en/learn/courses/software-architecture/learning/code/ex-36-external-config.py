# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 36: validate a deployment-provided configuration value."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
import os

# => This keeps the modeled rule explicit so its trade-off can be inspected.
timeout_seconds = int(os.environ.get("PAYMENT_TIMEOUT_SECONDS", "30"))
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert timeout_seconds > 0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(timeout_seconds)
