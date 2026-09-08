---
description: Scope and termination safeguards for the UI quality gate's finite discovery-fix-verification run.
when_to_use: Use when deciding whether a UI quality gate may start another pass.
---

# Bounded Run

- **One discovery**: Audit the full requested scope once. A clean discovery passes immediately.
- **At most one fix pass**: Re-validate findings, then fix only validated in-threshold findings.
- **One scoped verification**: Reproduce the original findings and smoke-test affected components;
  do not repeat full discovery.
- **Finite termination**: Unresolved originals or regressions produce `partial`; technical errors
  produce `fail`. Neither outcome starts another pass automatically.
- **Persistent triage**: Keep false positives and below-threshold findings in the report without
  treating them as reasons to rerun.
