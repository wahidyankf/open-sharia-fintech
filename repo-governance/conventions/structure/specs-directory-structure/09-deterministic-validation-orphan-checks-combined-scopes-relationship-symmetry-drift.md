---
title: "Deterministic Validation: Orphan Checks, Combined Scopes, Relationship Symmetry, and Drift Detection"
description: The reverse-direction step orphan check, combined multi-perspective coverage runs, DDD relationship symmetry checks, and the current (unimplemented) drift-detection commands
when_to_use: Read this when debugging an orphan-step coverage failure, wiring a combined gherkin-scopes coverage run, or checking a DDD relationship-symmetry finding.
category: explanation
subcategory: conventions
tags:
  - conventions
  - specs
  - gherkin
  - directory-structure
  - organization
  - c4-diagrams
  - openapi
  - c4
created: 2026-04-02
---

# Deterministic Validation: Orphan Checks, Combined Scopes, Relationship Symmetry, and Drift Detection

## Reverse-direction step orphan check (Fix #15)

Every `rhino-cli specs coverage` invocation enforces both directions:

- **Forward**: every Gherkin step has a matching impl.
- **Reverse**: every impl matcher has at least one matching Gherkin step.

Orphan impls fail the gate non-zero. There is no `--allow-orphan-steps` flag and no env var escape hatch — any orphan is either real drift or an extractor bug that must be fixed at source. The pre-flight audit ran across all 15 specs:coverage-wired projects in worktree as part of this plan and reached `FAIL=0` before merge.

The validator handles Scenario Outline forms in both directions: outline steps are emitted with `<placeholder>` tokens intact for forward matching against vitest-cucumber per-scenario impls, and Examples-table-expanded variants feed both directions so playwright-bdd regex-pattern impls binding expanded values count as covered. Comments in `.ts/.tsx` source are stripped before extraction (line comments only when at line start to preserve regex literals; block comments anywhere; strings preserved verbatim) so commented-out placeholder doc lines do not become false-positive orphan matches.

## Combined gherkin scopes per app

`rhino-cli specs coverage` accepts a variadic specs-dirs list (`specs coverage <specs-dir> [<specs-dir>...] <app-dir>`). Apps with multiple gherkin perspectives (ose-www has web + api; ayokoding-www has web + api + cli) declare a single combined run in `project.json` so impls shared across scopes don't false-positive on per-scope orphan checks.

## Expanded relationship symmetry (DDD validators)

`bcregistry/validator.go` flags asymmetric relationships for `customer-supplier`, `conformist`, `partnership`, and `shared-kernel` kinds. `anticorruption-layer` and `open-host-service` are intentionally one-way and silent. Unknown relationship kinds (e.g., typos like `shered-kernel`) produce an explicit "unknown relationship kind" finding via the new `checkRelationshipKinds` pass.

## Drift detection

Drift detection commands (`drift-routes`, `drift-endpoints`, `drift-contracts`) are **not currently implemented**. The placeholder command files were removed in the BDD+DDD tooling gap-fill plan (2026-05) because reservation-pattern stubs that print "Not yet implemented" mislead callers into believing functionality exists. If drift detection is later required, a new plan adds those commands back as real implementations rather than stubs. Track via the tooling backlog.
