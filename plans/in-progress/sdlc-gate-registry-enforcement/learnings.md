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

### Revalidate executable plan artifacts immediately before readiness review

**Observed**: The 2026-08-02 plan passed its checker, but by 2026-08-04 `beaver-nest` had changed its
repository allowlist, runtime configuration, F# source footprint, test-target isolation, environment
scanner, tests, and Gherkin coverage. During this readiness refresh it advanced again to
`cd2ec0e4d`, changing its complete package baseline, removing the Vite frontend's environment
contract, and increasing its Shell/F# inventory. Its root is also a bare repository, so
primary-checkout commands in the original Phase 0 and Phase 5 procedures were not executable there.

**Why it matters**: A clean planning audit is a point-in-time result. Plans that carry copy-ready
artifacts or cross-repository assumptions need an explicit live-state reconciliation before execution;
otherwise a mechanically correct copy step can revert newer work or fail before establishing its
baseline.

**Home**: to be triaged in Phase 6 — candidate is the plans convention's readiness or Phase 0
guidance.

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
