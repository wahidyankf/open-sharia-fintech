---
description: The three things a pull request adding code must state in its body — what the code buys, what it costs to maintain, and which simpler alternative was rejected.
when_to_use: Use when writing or reviewing the cost/benefit section of a pull request that adds code.
---

# The Obligation

A pull request that adds code carries a short justification in its body stating three things.

1. **What the code buys** — the concrete capability or defect fix, not the intention behind it.
   "Callers can now resume an interrupted upload" is an answer; "improves reliability" is not.
2. **What it costs to maintain** — what future readers and changers inherit. Name the real cost: a
   new dependency, a second code path that must stay in step, a format that now needs migrating.
3. **What simpler alternative was rejected, and why** — including doing nothing, configuring
   something that already exists, extending a caller instead, or deleting code instead.

Three sentences is usually enough. The trade must be made deliberately and left visible, not argued
at length. A section that restates the pull request title in three shapes has not answered it.

The `.github/pull_request_template.md` file carries the section, so the prompt appears on every pull
request. Delete the section only when the change adds no in-scope code.

## Why the Pull Request Body

The justification lives where the decision is made and reviewed, and where `git log` preserves it
against the merge commit. A comment in the source drifts from the code beside it; a plan document
expires on archival. The pull request body is the durable record of _why this exists_, reachable
from any line via blame.

## Related Documents

- [What Counts as Code](./what-counts-as-code.md) — whether the obligation applies at all.
- [Scrutiny and Enforcement](./scrutiny-and-enforcement.md) — how high the bar sits for this change.
