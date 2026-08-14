---
title: "Pre-Push/CI Gating, LLM Semantic Validation, Deterministic Offload, Manual Checklist, and Related Documentation"
description: The four gating surfaces that run specs validation, the LLM-driven semantic-validation layer, the deterministic-vs-LLM reasoning split, the manual review checklist, and related-convention links
when_to_use: Read this when checking which CI surfaces gate specs/ changes, what specs-checker validates semantically, or doing a manual review pass on a specs/ change.
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

# Pre-Push/CI Gating, LLM Semantic Validation, Deterministic Offload, Manual Checklist, and Related Documentation

## Pre-push + CI gating surfaces

Every `validate:specs-*` target runs on all four gating surfaces — no surface lags behind:

- `.husky/pre-push` (every developer push, single line)
- `.github/workflows/pr-quality-gate.yml` (every PR, dedicated `specs-gate` job in `quality-gate.needs:`)
- `.github/workflows/_reusable-www-test-local-deploy.yml` (called by the www cron deploys, `specs-gate` job in `deploy.needs:`)
- `.github/workflows/organiclever-app-test-local-deploy-stag.yml` (cron on `main`, `specs-gate` job in `deploy.needs:`)

`docs validate-links` is NOT gated by this plan — it scans the entire repo's markdown (repo-governance/, docs/, app READMEs) and is owned by a separate planned validator-unification effort.

After this plan ships, **zero specs/BDD/DDD scripts in `rhino-cli` are dead** — every command file under `apps/rhino-cli/src/commands/specs_*.rs`, `src/commands/ddd_*.rs`, and `src/commands/spec_coverage*.rs` is invoked by at least one Nx target or pre-push surface.

## LLM Semantic Validation (specs-checker)

`specs-checker` validates categories that require semantic judgment: narrative coherence, terminology drift, C4 diagram consistency, cross-folder contradictions, and PM-readability compliance. See [Specs Validation Workflow](../../../workflows/specs/specs-quality-gate.md).

## Deterministic Offload

The reasoning split between deterministic and LLM checks follows the principle that counting, path comparison, and file-system walking belong in Rust/deterministic tooling, not in LLM context. Categories tagged `[Deterministic]` in `specs-checker` shell out to `rhino-cli`; categories tagged `[LLM]` keep LLM-driven reasoning.

## Manual Verification Checklist

When reviewing changes to the `specs/` directory, verify:

- [ ] App spec tree uses the five-folder layout at the top level
- [ ] No flat-root artifacts remain (`be/`, `web/`, `cli/`, `c4/`, `contracts/` at root)
- [ ] BE, web, and CLI specs use domain subdirectories (never flat under `gherkin/`)
- [ ] Lib specs use package subdirectories under `gherkin/`
- [ ] `README.md` index files exist at every directory level
- [ ] New projects include only the folders their surface profile needs
- [ ] Folder listing in README follows canonical order: `product/`, `system-context/`, `containers/`, `components/`, `behavior/`

## Related Documentation

- [App README vs Specs Convention](../app-readme-vs-specs.md) — combined convention: content split rule, PM-readability contract, BDD/DDD/Contracts adoption
- [Specs-Application Sync Convention](../../../development/quality/specs-application-sync.md) — bidirectional sync between specs and application code
- [BDD Spec-Test Mapping](../../../development/infra/bdd-spec-test-mapping.md) — how specs map to test implementations
- [Three-Level Testing Standard](../../../development/quality/three-level-testing-standard.md) — unit, integration, and E2E testing levels
- [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md) — Gherkin writing standards for feature files
- [File Naming Convention](../file-naming.md) — general file naming patterns
- [Plans Organization Convention](../plans.md) — similar convention for plans/ directory structure
- [Specs Validation Workflow](../../../workflows/specs/specs-quality-gate.md) — iterative validation workflow
