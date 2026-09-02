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

Specs validation is declared in the `gates:` registry of `repo-config.yml`, never wired by hand.
`specs-gherkin-cardinality` and `specs-structure` both carry `ci-group: specs` and run on every
surface their entries declare:

- `.husky/pre-push` — `gate run --surface=pre-push` reads them from the registry
- `.github/workflows/pr-quality-gate.yml` — the `specs-structure` job in `quality-gate.needs:`
- `_reusable-www-test-local-deploy.yml` and `_reusable-app-test-local-deploy-stag.yml` — the
  `specs-gate` job in `deploy.needs:`, called by the www and app cron deploys

**No specs command in `rhino-cli` is dead** — every specs module is reachable from a `SpecsCommands`
variant, and every variant is invoked by an Nx target or registry gate.

## LLM Semantic Validation (specs-checker)

`specs-checker` validates categories that require semantic judgment: narrative coherence, terminology drift, C4 diagram consistency, cross-folder contradictions, and PM-readability compliance. See [Specs Validation Workflow](../../../workflows/specs/specs-quality-gate.md).

## Deterministic Offload

The reasoning split between deterministic and LLM checks follows the principle that counting, path comparison, and file-system walking belong in Rust/deterministic tooling, not in LLM context. Categories tagged `[Deterministic]` in `specs-checker` shell out to `rhino-cli`; categories tagged `[LLM]` keep LLM-driven reasoning.

## Manual Verification Checklist

When reviewing changes to the `specs/` directory, verify:

- [ ] Every deployed surface has a logical owner corpus at the product root
- [ ] No flat-root artifacts remain (`be/`, `web/`, `cli/`, `c4/`, `contracts/` at root)
- [ ] BE, web, and CLI specs use domain subdirectories (never flat under `gherkin/`)
- [ ] Lib specs use package subdirectories under `gherkin/`
- [ ] `README.md` index files exist at every directory level
- [ ] New projects include only the folders their surface profile needs
- [ ] Entry listing in a corpus README follows canonical order: `architecture.md`, `contracts/`, `behaviors/`

## Related Documentation

- [App README vs Specs Convention](../app-readme-vs-specs.md) — combined convention: content split rule, PM-readability contract, BDD/Contracts adoption
- [Specs-Application Sync Convention](../../../development/quality/specs-application-sync.md) — bidirectional sync between specs and application code
- [BDD Spec-Test Mapping](../../../development/infra/bdd-spec-test-mapping.md) — how specs map to test implementations
- [Three-Level Testing Standard](../../../development/quality/three-level-testing-standard.md) — unit, integration, and E2E testing levels
- [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md) — Gherkin writing standards for feature files
- [File Naming Convention](../file-naming.md) — general file naming patterns
- [Plans Organization Convention](../plans.md) — similar convention for plans/ directory structure
- [Specs Validation Workflow](../../../workflows/specs/specs-quality-gate.md) — iterative validation workflow
