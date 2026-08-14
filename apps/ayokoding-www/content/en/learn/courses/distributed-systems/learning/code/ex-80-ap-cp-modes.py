"""Runnable artifact for distributed-systems Example 80."""

from __future__ import annotations

partitioned: bool = True
cp_result: str = "blocked" if partitioned else "committed"
ap_result: str = "accepted-locally" if partitioned else "committed"
# => One operation exposes the partition-time AP/CP behavior choice.
assert cp_result == "blocked" and ap_result == "accepted-locally"
print((cp_result, ap_result))
