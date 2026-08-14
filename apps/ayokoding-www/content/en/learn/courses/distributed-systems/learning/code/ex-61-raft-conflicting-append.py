"""Runnable artifact for distributed-systems Example 61."""

from __future__ import annotations

local_prior_term: int = 3
request_prior_term: int = 2
accepted: bool = local_prior_term == request_prior_term
# => A mismatched prior term rejects the conflicting append.
assert not accepted
print(accepted)
