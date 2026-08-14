# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 80."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
partitioned: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
cp_result: str = "blocked" if partitioned else "committed"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
ap_result: str = "accepted-locally" if partitioned else "committed"
# => One operation exposes the partition-time AP/CP behavior choice.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert cp_result == "blocked" and ap_result == "accepted-locally"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((cp_result, ap_result))
