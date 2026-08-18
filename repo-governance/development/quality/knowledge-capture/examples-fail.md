---
title: "Examples (continued)"
description: "FAIL examples of knowledge capture."
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
when_to_use: "Use for an incorrect knowledge-capture example."
---

# Examples (continued)

## FAIL: Silent absence

```markdown
<!-- learnings.md does not exist; delivery.md has no Knowledge Capture phase; no explanation given -->
```

`plan-checker` flags this at MEDIUM: the phase is mandatory, and its absence carries no explicit
"none" record.

## FAIL: Code change landed inline instead of backlogged

```markdown
**Routing**: `apps/organiclever-be` (code) — routed INLINE, landed in commit `def5678` of this
governance plan's PR.
```

This is a **plan-execution-checker** blocking finding: a code-homed learning must be filed as a
separate `plans/backlog/` plan, never landed inline, regardless of how small the fix looks.

## FAIL: Secret leaked into learnings.md

```markdown
## Learning: the staging database connection string is postgres://admin:hunter2@10.0.4.12:5432/app
```

Fails the secret/sensitivity gate outright — discard, or rewrite as
`postgres://<user>:<placeholder>@<staging-db-host>:5432/<db-name>` if the underlying insight (e.g.,
"the staging connection string format differs from production") is itself worth keeping.

## FAIL: Infra-private content cross-routed to a public repo

```markdown
**Routing**: `repo-governance/` in `ose-public` — this k3s node's real hostname handling should be
documented here.
```

Fails the repo-relevance gate: infra-specific content (a real k3s node/hostname) must stay in
`ose-private` only, never in `ose-public`.
