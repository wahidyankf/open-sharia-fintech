---
title: "Learnings — SDLC Gate Registry Enforcement"
description: Knowledge capture during execution, triaged to a permanent home or discarded at Phase 6
category: explanation
subcategory: plans
tags:
  - learnings
  - ci-cd
created: 2026-08-02
---

# Learnings — SDLC Gate Registry Enforcement

Populated during execution. Each entry is triaged in Phase 6 to a home in `docs/` or
`repo-governance/`, or discarded with a stated reason.

## Format

```markdown
### <short title>

**Observed**: what happened
**Why it matters**: the general rule behind the instance
**Home**: `docs/...` / `repo-governance/...` / discarded — reason
```

## Entries

### Pre-seeded from the 2026-08-02 audit

**Observed**: The Gate Composition Rule was ratified as prose plus markdown tables and drifted in
both directions in all four repos within roughly a month, without any single deliberate decision to
diverge.

**Why it matters**: A normative rule expressed only in prose degrades silently. The repo already knew
this — it is why harness bindings are generated and validated rather than hand-synced. The lesson is
that the generate-and-validate pattern should be the default for any invariant spanning more than one
file, not a special case reserved for bindings.

**Home**: to be triaged in Phase 6 — candidate is
`repo-governance/development/practice/` as a general "mechanize the invariant" practice.

### Reconciliations found porting the engine into the `beaver-nest` fork

**Observed**: (populate during Phase 5)

**Why it matters**: (populate)

**Home**: (populate)
