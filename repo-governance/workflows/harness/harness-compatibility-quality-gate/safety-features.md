---
description: Infinite-loop prevention, research-quality safeguards, false-positive protection, and error recovery for the harness compatibility gate.
when_to_use: Use when auditing this workflow's guardrails against runaway iteration or stale research.
---

# Safety Features

**Infinite Loop Prevention**:

- `max-iterations` defaults to 7 — override with a higher value for more attempts
- Workflow terminates with `partial` if the limit is reached
- Tracks iteration count for observability
- Escalation warning at iteration 5 if not converging

**Research Quality Safeguards**:

- Checker cites source URL and retrieval date for every upstream fact in the audit report
- Fixer re-validates each finding before applying (prevents acting on stale research)
- Out-of-scope findings are surfaced to the human rather than silently skipped

**False Positive Protection**:

- Fixer re-validates each finding before applying
- Progressive writing ensures audit history survives across iterations
- Checker logs whether research was reused or refreshed per harness

**Error Recovery**:

- Continues to verification even if some fixes fail
- Reports which fixes succeeded and which were flagged for human resolution
- Generates final report regardless of status
