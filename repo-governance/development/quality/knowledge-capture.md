---
description: Standards for capturing generalizable learnings during plan execution in a transient learnings.md log, triaging each through an open-ended principle-based routing matrix, and enforcing two safety gates before any learning reaches a durable home
when_to_use: "Use when a plan surfaces a generalizable learning and you need to capture or route it."
---

# Knowledge Capture Convention

This convention defines how a generalizable learning discovered during plan execution is captured, triaged, and routed to a durable home -- gated by two mandatory safety checks.

## Documents

- [Principles and Conventions Implemented/Respected](./knowledge-capture/principles-and-conventions-implemented-respected.md) — Principles/conventions this convention implements. Use when tracing this convention's rationale.
- [The Rule](./knowledge-capture/the-rule.md) — The core knowledge-capture rule. Use for the exact wording of the rule.
- [The Transient `learnings.md` Running Log](./knowledge-capture/the-transient-learnings-md-running-log.md) — How the transient learnings.md log works. Use when maintaining a plan's learnings.md log.
- [The Triage Rubric: Open-Ended, Principle-Based Routing](./knowledge-capture/the-triage-rubric-open-ended-principle-based-routing.md) — The rubric for routing a learning to its home. Use when triaging a captured learning.
- [The Code-Routing Downstream Rule](./knowledge-capture/the-code-routing-downstream-rule.md) — Routing for a learning implying a code change. Use when a learning implies a code change.
- [Routing Timing: Destination-Aware (Inline vs. Ideas)](./knowledge-capture/routing-timing-destination-aware-inline-vs-ideas.md) — Inline routing versus an explicitly authorized `plans/ideas/` two-pager; Knowledge Capture never creates backlog directly.
- [The Two Safety Gates (HARD — run before routing)](./knowledge-capture/the-two-safety-gates-hard-run-before-routing.md) — The two mandatory pre-routing safety gates. Use before routing any learning.
- [Mandatory + Explicit "None" Escape](./knowledge-capture/mandatory-explicit-none-escape.md) — Why plans must state "no learnings" explicitly. Use when a plan has no learnings to record.
- [Anti-Theater Guardrails](./knowledge-capture/anti-theater-guardrails.md) — Guardrails against performative knowledge capture. Use when a learnings.md entry looks performative.
- [The Transient-Log Caveat](./knowledge-capture/the-transient-log-caveat.md) — Why learnings.md is never a durable home. Use when deciding if content still needs routing.
- [What Gets Validated](./knowledge-capture/what-gets-validated.md) — What plan-execution-checker validates here. Use to know what the validation gate checks.
- [Examples](./knowledge-capture/examples-pass.md) — PASS examples of knowledge capture. Use for a correct knowledge-capture example.
- [Examples (continued)](./knowledge-capture/examples-fail.md) — FAIL examples of knowledge capture. Use for an incorrect knowledge-capture example.
- [Related Documentation](./knowledge-capture/related-documentation.md) — Related plan, post-mortem, and safety conventions. Use for a related plan or safety-gate convention.

## Exemptions

Pure-docs and trivial plans MAY skip elaborate Knowledge Capture — this mirrors the existing
exemption pattern in [Feature Change Completeness](./feature-change-completeness/two-paths-with-a-plan-and-without-a-plan.md#two-paths-with-a-plan-and-without-a-plan)
for the specs/Gherkin two-path rule. A one-line rename, a single broken link fix, or an equivalently
trivial plan does not require a populated `learnings.md`; the explicit "none" escape above (or an
equally explicit note in `delivery.md`) satisfies the requirement without inventing insight from a
change that had none to offer.
