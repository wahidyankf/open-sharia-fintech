# Cross-Cycle Behavior and External Fact Verification

## Cross-Cycle Behavior

Each cycle, `pr-review-scout-maker` re-runs its own risk-tier classification, shared-context
assembly, and prior-cycle thread-resolution read upstream, and this agent re-runs its own
dedup/re-categorize/filter/verify pipeline over the resulting raw findings — against the **full
PR**, not just the delta — while deduplicating against the prior cycle's already-posted,
already-resolved findings.

**Human-dismissal respect (sharpened rule)**. Never include, in a new cycle's consolidated
review, a finding a human has explicitly dismissed ("won't fix" / "I disagree") on its thread in
a prior cycle — this is exactly the prior-cycle thread-resolution read duty `pr-review-scout-maker`
applies before fanning out each cycle; this agent respects that resolution state at post time and
never lets a specialist's re-raised version of that same finding survive the
reasonableness-filter.

A fixer rejection carrying `effect: stale-cycle-only` resolves only an obsolete cycle's thread;
it never suppresses the underlying finding on the fresh head. Preserve any independently verified
version through the filter and assign it a new cycle finding ID.

## External Fact Verification

You may call the [`web-researcher`](../../../agents/web/web-researcher.md) agent for external fact
verification during tool-verify — for example, confirming a claimed API behavior, a library's
current signature, or a security advisory a specialist's finding references. Use in-context
`WebFetch`/`WebSearch` only for single-shot verification against a known authoritative URL;
delegate to `web-researcher` for anything requiring multi-page research, per the
[Web Research Delegation Convention](../../../../repo-governance/conventions/writing/web-research-delegation.md).
