---
description: "Read the full incoming diff and assess its impact whenever commits not previously on the branch land."
when_to_use: "Read this index to find the right Integration Diff Review Convention child document."
---

# Integration Diff Review Convention

- [Principles and Conventions Implemented](./principles-and-conventions-implemented.md) — The principles and companion conventions the integration diff review convention implements and respects. Use when tracing why integration diff review exists back to the principles and conventions it respects.
- [The Rule and Reading Checklist](./the-rule-and-reading-checklist.md) — The five-step checkpoint for reconciling an incoming diff with task, plan, assumptions, ledger, and verification. Use immediately after a rebase, pull, merge, cherry-pick, or fast-forward introduces commits not previously on the branch.
- [Commands and Agent Responsibilities](./commands-and-agent-responsibilities.md) — The git commands for identifying and diffing an incoming range after each integration operation, and who is responsible for reviewing it. Use when you need the exact command for the integration operation that just ran, or to confirm whose responsibility the review is.
- [Forbidden Actions and Examples](./forbidden-actions-and-examples.md) — Actions that violate the integration diff review convention, and worked pass/fail examples of reviewing after a rebase, pull, or fast-forward. Use when checking whether a resumed task actually reviewed its incoming diff, or when writing a worked example of doing so.
