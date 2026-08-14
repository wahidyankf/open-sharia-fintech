# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 61."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
local_prior_term: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
request_prior_term: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = local_prior_term == request_prior_term
# => A mismatched prior term rejects the conflicting append.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)
