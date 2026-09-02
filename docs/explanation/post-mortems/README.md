---
title: Post-Mortems
description: Blameless incident retrospectives for the open-sharia-enterprise software platform
category: explanation
tags:
  - index
  - explanation
  - post-mortems
  - incidents
  - reliability
created: 2026-06-05
---

# Post-Mortems

**Blameless incident retrospectives.** Each post-mortem explains what happened, why, and what we changed so the same failure does not recur — and so the reasoning survives past the people who were in the room.

## What is a Post-Mortem?

Per the [Diátaxis framework](../../../repo-governance/conventions/structure/diataxis-framework.md), post-mortems are **understanding-oriented** (explanation): they answer "why did this happen?" rather than "how do I do X?". They are written **blameless** — focused on systems and contributing factors, never individuals.

Post-mortems serve two purposes:

1. **Learning** — document what actually happened and why decisions made sense at the time, so the team builds accurate mental models of its systems.
2. **Improvement** — convert that learning into concrete, owned, prioritized action items that reduce the probability or impact of similar incidents.

## Authoritative Standard

The full rules — mandatory sections, severity scale, action-item tracking, `doc_status` lifecycle, naming, and the no-secrets requirement — live in the [Post-Mortem Convention](../../../repo-governance/conventions/structure/post-mortems.md). This page is the practical working surface: a copy-paste template and the index. When the two disagree, the convention wins.

## Template

Copy this skeleton when starting a new post-mortem. Section order is mandatory; sections marked _(optional)_ may be dropped for low-severity incidents. See the [Post-Mortem Convention](../../../repo-governance/conventions/structure/post-mortems.md) for what each section must contain, and the [worked example](./2026-05-03-amazonq-bindings-prettier-parity-guard-break.md) — the Amazon Q bindings Prettier parity-guard break post-mortem.

```markdown
---
title: "Post-Mortem: <System> — <Short Failure>"
description: <one sentence>
category: explanation
subcategory: post-mortem
doc_status: draft # draft → reviewed → closed (document lifecycle, not incident status)
tags:
  - post-mortem
  - <system-tag>
created: YYYY-MM-DD
---

# Post-Mortem: <System> — <Short Failure>

| Field              | Value                            |
| ------------------ | -------------------------------- |
| Incident date      | YYYY-MM-DD                       |
| Investigation date | YYYY-MM-DD                       |
| Severity           | Sev-N — Label (see convention)   |
| Status             | Investigating / Resolved         |
| Author             | <role> (blameless retrospective) |

## Summary

<!-- 2–4 sentences: what failed, how long it lasted, and the outcome. Write last, place first. -->

## Impact

<!-- Quantify: services/users affected, duration, MTTD and MTTR (or "unknown — no alerting"). -->

## Detection

<!-- How discovered. Append category label: Manual | Monitoring Alert | Automated Health Check | User Report -->

## Timeline

<!-- Absolute timestamps with stated timezone (WIB UTC+7). -->

| Time (WIB UTC+7) | Event |
| ---------------- | ----- |
| YYYY-MM-DD HH:MM | ...   |

## Root Cause

<!-- The deepest systemic condition that made the incident possible. Explains WHY the trigger was
able to cause harm. Distinct from Trigger. Never name a person as root cause. -->

## Trigger

<!-- The proximate event that started the incident chain — "what pulled the thread."
Distinct from Root Cause. -->

## Contributing Factors

<!-- Bullet list of systemic conditions that made the incident worse or recovery harder.
These are conditions, not causes to blame. -->

## Resolution & Mitigations

<!-- What restored service. Distinguish: applied fix (this incident) vs open root-cause fix
(tracked in Action Items). -->

## Action Items

| #   | Action | Owner | Priority | Ticket | Status |
| --- | ------ | ----- | -------- | ------ | ------ |
| 1   | ...    | ...   | P0       | —      | Open   |

## What Went Well

<!-- What limited impact. Also note "where we got lucky" — luck is latent risk, not silent celebration. -->

## Lessons Learned

<!-- 2–5 bullets. Key insights that generalize beyond the immediate fix. -->

## References

<!-- CI run logs, deployment dashboards, related plans, related post-mortems, external sources. -->

## Background

<!-- (optional) Relevant system context a reader outside the incident would need.
May appear before Summary when substantial up-front context is required. -->

## Supporting Data

<!-- (optional) Graphs, log excerpts, metrics snapshots. Use Mermaid or fenced code blocks.
Never paste secrets or credential material — see no-secrets rule. -->
```

## Filing Conventions

- **Filename**: `YYYY-MM-DD-<system>-<short-failure>.md` where the date is the **incident date**, not the writing date. All components are lowercase kebab-case. Example: `2026-05-03-amazonq-bindings-prettier-parity-guard-break.md`.
- **Layout**: flat directory — no subdirectories inside `docs/explanation/post-mortems/`. Revisit folder grouping (e.g., by year) only if volume grows.
- **Timing**: write promptly while details are fresh (within a few days of the incident).
- **`doc_status`**: `draft` → `reviewed` → `closed`. Advance to `closed` only once all P0 action items resolve. This is the document lifecycle, distinct from the incident `Status` field in the metadata table.
- **No secrets**: never commit real tokens, passwords, API keys, connection strings, or other sensitive values to any git-tracked file. Use placeholders per the [No Secrets in Git](../../../repo-governance/conventions/security/no-secrets-in-committed-files.md) convention, and state where the real value lives. This applies without exception to timelines, log excerpts, and configuration references in post-mortems.
- **Blameless tone**: describe systems, conditions, and decisions — not individuals. See the blameless principle in the [Post-Mortem Convention](../../../repo-governance/conventions/structure/post-mortems.md).

## Index

- **[ayokoding-www Calculator — Bland, Buggy UI Shipped Past Green Gates](./2026-06-19-ui-design-parity-shipped-past-green-gates.md) — A user-facing calculator was validated to zero findings, archived to `plans/done/`, and deployed bland, off-design, and carrying two calculation bugs while every automated gate was green. Root cause: the done/archival criterion had no production visual or value-bearing sign-off. Fixed and codified as the [User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md) (14 rules).** (2026-06-19, Sev-3)
- [Amazon Q Bindings Prettier Parity Guard Break](./2026-05-03-amazonq-bindings-prettier-parity-guard-break.md) — Prettier's post-tool hook reformatted emitter-generated `.amazonq/**` binding artifacts, breaking the `validate:cross-vendor-parity` byte-equality guard on every Edit operation. Fixed by adding emitter-generated paths to `.prettierignore`. (2026-05-03, Sev-3)
