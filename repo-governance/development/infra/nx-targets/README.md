---
title: "Nx Target Standards"
description: "Standardized Nx target definitions for apps and libs in the monorepo"
when_to_use: "Read this index to find the right Nx Target Standards child document."
---

# Nx Target Standards

- [Execution Model](./01-execution-model.md) — Explains the mermaid-diagrammed pre-push/PR quality-gate flow and the scheduled/on-demand testing tiers that Nx targets execute.
- [Principles and Conventions Implemented/Respected](./02-principles-and-conventions.md) — Lists the software-engineering principles and repo conventions that the Nx target scheme implements.
- [Target Naming Standards — Canonical Target Reference (Lifecycle Targets)](./03-target-naming-canonical-names.md) — The canonical target-name reference table for the core lifecycle and quality-gate targets (build through test:e2e), with purpose and when-required columns.
- [Target Naming Standards — Canonical Target Reference (E2E and Utility Targets)](./04-target-naming-canonical-names-e2e-and-utility.md) — The canonical target-name reference table for the remaining targets — E2E UI/report variants, dev/start/run, and codegen/docs/install/clean — with purpose and when-required columns.
- [Naming Rules](./05-target-naming-rules.md) — The naming rules governing dev/start/test:\* target names and the colon-versus-hyphen separator convention.
- [`{domain}:{work}` Naming for Governance and Validation Targets](./06-domain-work-naming-for-governance-targets.md) — Defines the {domain}:{work} naming scheme for governance, validation, lint, and format targets, with the canonical target list.
- [Formatting and File-Type Linting (lint-staged, not Nx targets)](./07-formatting-and-file-type-linting.md) — Explains why formatting and several file-type lint checks run as lint-staged entries instead of Nx targets, with the glob-to-tool tables.
- [Tag Convention — Four-Dimension Scheme](./08-tag-convention-four-dimension-scheme.md) — Defines the four required project.json tag dimensions (type, platform, language, domain) and the special-case rules for Rust libs and tooling projects.
- [Tag Convention — Tags, Examples, and Anti-Patterns](./09-tag-convention-current-tags-and-examples.md) — The current per-project tag table, two worked tag-declaration examples, and the tag anti-patterns to avoid.
- [Mandatory Targets — Summary Matrix](./10-mandatory-targets-summary-matrix.md) — The per-project-type summary matrix of which mandatory targets are real versus echo, plus backend typecheck examples and CI schedules.
- [Mandatory Targets — Mandatory-Six and Required-Where-Applicable Targets](./11-mandatory-targets-all-projects-six-and-required.md) — The mandatory-six targets every registered project must declare, and the required-where-applicable targets declared only when a condition applies.
- [Mandatory Targets — test:quick Composition and Gate-Surface Rule](./12-mandatory-targets-all-projects-quick-and-gate.md) — The canonical five-step test:quick composition with a worked rhino-cli example, and the gate-surface / scheduled-tier rule.
- [Mandatory Targets — Type, Build, Server, and Unit-Test Requirements](./13-mandatory-targets-type-build-server-unit.md) — Requirements for typecheck on statically typed projects, build on compiled/bundled projects, dev/start on server apps, and test:unit.
- [Projects with Integration Tests](./14-mandatory-targets-integration-tests.md) — The two integration-test patterns (Docker+PostgreSQL for API backends, in-process mocking elsewhere) and the Rust CLI two-test-file convention.
- [Mandatory Targets — CLI and E2E Test Projects](./15-mandatory-targets-cli-e2e.md) — The run/install targets required on CLI applications and the install/test:e2e/test:e2e:ui/test:e2e:report targets required on \*-e2e projects.
- [Specs:Behavior:Coverage Projects](./16-mandatory-targets-specs-behavior-coverage.md) — The specs:behavior:coverage command-flag reference and per-project coverage-status table for Gherkin behavior-level validation.
- [Accessibility Testing](./17-mandatory-targets-accessibility-testing.md) — The two-level accessibility testing requirement (static a11y linting and runtime axe-core E2E tests) for UI projects.
- [Workspace Defaults, Caching, and Build Output](./18-workspace-defaults-caching-build-output.md) — The nx.json targetDefaults block, the per-target caching-rules table, and the build output directory conventions.
- [Cache and Inputs Convention — Canonical Inputs](./19-cache-and-inputs-convention-canonical.md) — Why explicit inputs are required for correct cache invalidation, with canonical Rust/Go input examples for CLI apps and API backends.
- [Cross-Repo rhino-cli Byte-Identity Standard](./20-cache-cross-repo-byte-identity.md) — The four rules holding apps/rhino-cli to a stricter, byte-identical standard across ose-public and ose-private.
- [Codegen Dependency Chain](./21-codegen-dependency-chain.md) — The codegen -> typecheck / codegen -> build dependency chain for apps with OpenAPI contract specs.
- [Anti-Patterns — Echo Placeholders](./22-anti-patterns-echo-placeholders.md) — Clarifies that echo placeholders for test:unit/test:integration/test:e2e are required, not an anti-pattern -- omitting the mandatory-six is.
- [Target Anti-Patterns](./23-target-anti-patterns.md) — The catalog of Nx target anti-patterns to avoid -- non-standard names, omitted mandatory targets, heavy test:quick, and more.
- [Principles Traceability](./24-principles-traceability.md) — Maps each major Nx target design decision to the software-engineering principle it implements.
