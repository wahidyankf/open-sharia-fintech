---
title: "Nx Target Naming Convention"
description: Derivation rules for Nx target names, covering the {domain}:{work} scheme for governance and validation targets and the lifecycle naming scheme for build/test targets
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - naming
  - conventions
created: 2026-06-13
---

# Nx Target Naming Convention

Defines how Nx target names are derived for all projects in the workspace. Two naming schemes
apply, depending on the target's purpose: the **lifecycle scheme** for build, test, and
runtime targets, and the **`{domain}:{work}` scheme** for governance, validation, lint, and
format targets.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Target names encode their scope and operation, making `nx affected -t specs:coverage` more
  self-describing than `nx affected -t spec-coverage`.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**:
  Two schemes cover all cases. No per-project inventions. A reader who knows the scheme can
  predict any target name.

## Conventions Implemented/Respected

- **[Nx Target Standards](./nx-targets.md)**: The full required target set per project type
  and caching rules are defined there. This document covers only the naming derivation rule.

## Scheme 1 — Lifecycle Targets

Lifecycle targets describe the project's build and test pipeline. Names are short verbs or
`verb:qualifier` pairs. These are constant across all project types (every project that has
unit tests uses `test:unit`, not `test-unit`, not `unit`, not `unit_tests`).

| Pattern              | Examples                                                                       |
| -------------------- | ------------------------------------------------------------------------------ |
| `{verb}`             | `build`, `lint`, `typecheck`, `dev`, `start`, `run`                            |
| `{verb}:{qualifier}` | `test:quick`, `test:unit`, `test:integration`, `test:e2e`, `test:e2e:ui`       |
| `specs:coverage`     | Special: governance target that behaves like lifecycle (runs in pre-push + CI) |

**Rules**:

- Use `dev` for development server — never `serve` or `start:dev`.
- Use `start` for production server — never `serve`.
- Separate qualifiers with `:` — never `-` or `_`.
- All names are lowercase kebab-case.

## Scheme 2 — `{domain}:{work}` for Governance and Validation Targets

Governance, validation, lint, and format targets use `{domain}:{work}` where:

- **domain**: lowercase noun naming the subject or scope of the check (e.g., `specs`,
  `links`, `mermaid`, `env`, `naming`, `governance`, `cross-vendor`, `harness`,
  `format`, `msrv`).
- **work**: lowercase verb phrase naming the operation. Pure checks end in `-validation`.
  Bare operations use a single verb (`check`).

**Rule**: do not invent `validate:{thing}` prefixes. The old `validate:*` naming scheme was
retired in P10 (2026-06-12); any `validate:` target in `project.json` or a caller script
is a bug.

### Canonical Governance and Validation Targets

All defined on `rhino-cli`. Other projects expose `specs:coverage` only.

| Target                                 | Subject                   | Operation                                                     |
| -------------------------------------- | ------------------------- | ------------------------------------------------------------- |
| `specs:coverage`                       | Gherkin specs             | Validate every step has a step definition                     |
| `specs:tree-validation`                | Specs directory tree      | Validate structure matches app registrations                  |
| `specs:counts-validation`              | Spec scenario/step counts | Validate counts meet thresholds                               |
| `specs:adoption-validation`            | App registrations         | Validate every app has a spec directory                       |
| `specs:gherkin-cardinality-validation` | Gherkin keyword usage     | Validate keyword cardinality within bounds                    |
| `links:validation`                     | All `.md` files           | Validate internal + anchor links                              |
| `mermaid:validation`                   | Mermaid diagrams          | Validate width, label length, syntax (flowchart + state)      |
| `headings:hierarchy-validation`        | Prose `.md` files         | Validate heading nesting on allowlist paths                   |
| `env:validation`                       | `.env.example` files      | Validate against `env-contract:` section in `repo-config.yml` |
| `naming:harness-validation`            | Agent definition files    | Validate names match naming convention                        |
| `naming:workflows-validation`          | Workflow files            | Validate names match naming convention                        |
| `governance:vendor-audit-validation`   | `repo-governance/` docs   | Validate no vendor-specific content leakage                   |
| `cross-vendor:parity-validation`       | All binding trees         | Validate cross-vendor behavioral parity                       |
| `harness:bindings-validation`          | Binding artifacts         | Validate `.claude/` ↔ `.opencode/` ↔ `.amazonq/` parity       |
| `format:check`                         | Rust source               | `rustfmt --check`                                             |
| `compat:min-version`                   | Rust toolchain            | Minimum Supported Rust Version compatibility                  |

### Derivation Examples

| Subject scope              | Operation      | Derived target                       |
| -------------------------- | -------------- | ------------------------------------ |
| `specs` (Gherkin)          | check adoption | `specs:adoption-validation`          |
| `links` (markdown)         | validate       | `links:validation`                   |
| `mermaid` (diagrams)       | validate       | `mermaid:validation`                 |
| `governance` (vendor docs) | audit          | `governance:vendor-audit-validation` |
| `format` (Rust fmt)        | check          | `format:check`                       |

### Anti-Patterns

| Forbidden                 | Correct                     | Reason                                 |
| ------------------------- | --------------------------- | -------------------------------------- |
| `validate:mermaid`        | `mermaid:validation`        | `validate:*` prefix abolished          |
| `validate:links`          | `links:validation`          | same                                   |
| `validate:specs-adoption` | `specs:adoption-validation` | same                                   |
| `spec-coverage`           | `specs:coverage`            | Hyphen dropped; domain clarified       |
| `fmt:check`               | `format:check`              | Domain must be the noun (`format`)     |
| `check:msrv`              | `compat:min-version`        | Verb follows domain: `{domain}:{verb}` |

## Scheme 3 — CLI Command Naming: `{domain} {noun…} {verb}` (Verb-Last)

All `rhino-cli` subcommands follow a verb-last grammar introduced in §2a of the SDLC-parity plan
(2026-06-26). The terminal token of every command path is the **verb** — `validate`, `generate`,
`clean`, `scaffold`, or similar.

**Pattern**: `{domain} {sub-domain…} {noun} {verb}`

| Old (verb-middle)                            | New (verb-last)                              |
| -------------------------------------------- | -------------------------------------------- |
| `convention validate emoji`                  | `convention emoji validate`                  |
| `convention validate license`                | `convention license validate`                |
| `harness validate bindings`                  | `harness bindings validate`                  |
| `harness validate duplication`               | `harness duplication validate`               |
| `harness validate naming`                    | `harness naming validate`                    |
| `harness validate sync`                      | `harness sync validate`                      |
| `harness validate claude`                    | `harness claude validate`                    |
| `harness validate instruction-size`          | `harness instruction-size validate`          |
| `harness generate bindings`                  | `harness bindings generate`                  |
| `md validate links`                          | `md links validate`                          |
| `md validate mermaid`                        | `md mermaid validate`                        |
| `md validate heading-hierarchy`              | `md heading-hierarchy validate`              |
| `md validate naming`                         | `md naming validate`                         |
| `md validate frontmatter`                    | `md frontmatter validate`                    |
| `md validate frontmatter-dates`              | `md frontmatter-dates validate`              |
| `md validate readme-index`                   | `md readme-index validate`                   |
| `repo-governance validate vendor`            | `repo-governance vendor validate`            |
| `repo-governance validate layer-coherence`   | `repo-governance layer-coherence validate`   |
| `repo-governance validate traceability`      | `repo-governance traceability validate`      |
| `specs validate gherkin-cardinality`         | `specs gherkin-cardinality validate`         |
| `lang java validate null-safety-annotations` | `lang java null-safety-annotations validate` |

**Cross-domain moves** (domain changes, not just verb position):

| Removed                                | Replaced by                                    |
| -------------------------------------- | ---------------------------------------------- |
| `convention validate instruction-size` | `harness instruction-size validate`            |
| `workflows validate naming`            | `repo-governance workflows naming validate`    |
| `harness sync opencode`                | `harness bindings generate --harness opencode` |
| `harness emit amazonq`                 | `harness bindings generate --harness amazonq`  |
| `convention validate agents-md-size`   | Removed (superseded by `instruction-size`)     |
| `git pre-commit`                       | Removed (pre-commit steps call tools directly) |

**Stable commands** (already verb-last or single-word noun, unchanged):

- `env validate`, `env init`, `env backup`, `env restore`
- `env staged-guard validate`
- `specs structure validate`, `specs behavior-coverage validate`, `specs domain-coverage validate`
- All `{domain} audit` leaf commands

**Rules**:

- Verbs (`validate`, `generate`, `clean`, `scaffold`) are always the LAST token.
- Nouns are kebab-case (`heading-hierarchy`, `gherkin-cardinality`, `null-safety-annotations`).
- Cross-domain moves require removing the old path entirely — no aliases are kept.
- Any new CLI command added must follow this verb-last pattern.

## Lint-Staged Membership Rule

A check belongs in `lint-staged` **if and only if** it satisfies **both** criteria:

1. **File-type-based**: triggered by a path glob (for example, `*.md`, `*.sh`, `*.rs`).
2. **Per-file isolated**: its result does not depend on the content of any other file — it
   runs correctly on only the changed files.

Checks that pass both criteria parallelise cleanly over the staged set and require no project
graph. Everything else belongs in an Nx target (project-scoped) or a dedicated hook step.

### Qualifying Checks

The following checks satisfy both criteria and belong in `lint-staged`:

- **Formatters**: `prettier`, `rustfmt`, `fantomas`, `gofmt`, `ruff format`, `dart format`,
  `cljfmt`, `csharpier`, and `mix format` (via wrapper for project-root config).
- **File-type linters**: `shellcheck` (`*.sh`), `hadolint` (`Dockerfile`/`*.Dockerfile`),
  `actionlint` (`.github/workflows/*.{yml,yaml}`).
- **Per-file markdown validators**: `markdownlint-cli2`, `md mermaid validate`,
  `md heading-hierarchy validate`.
- **Gherkin cardinality**: `specs gherkin-cardinality validate` (`*.feature`).

### Non-Qualifying Checks

Checks that fail one or both criteria stay outside `lint-staged`:

| Check                             | Fails because                                                                                           | Placement                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `md links validate`               | Not per-file isolated — adding, deleting, or renaming any `.md` file can break links in untouched files | Repo-wide `rhino-bin.sh` gate (pre-push / PR / main) |
| `harness:bindings-generate`       | Not file-type-based — regenerates all binding trees from the whole `.claude/` tree                      | Dedicated `rhino-bin.sh` step (pre-commit step 3)    |
| `test:quick`, `typecheck`, `lint` | Not file-type-based — project-scoped compile / test                                                     | Nx target (pre-push onward)                          |

### Consequences for the Nx Target Set

Applying this rule removes several Nx targets from `project.json` files:

- **No per-project `format` or `format:check` Nx target** — formatting runs as lint-staged
  file-type entries, not as per-project targets.
- **No `shell:lint`, `dockerfiles:lint`, or `actions:lint` Nx targets** — `shellcheck`,
  `hadolint`, and `actionlint` run as lint-staged file-type entries.

### Deliberate Carve-Out: `env staged-guard validate`

`env staged-guard validate` satisfies both criteria (file-type-based on `*.env*` globs;
per-file isolated because rejection is decided from the path alone). Despite satisfying the
rule, it remains a **dedicated first pre-commit step** (direct `rhino-bin.sh`, never a
lint-staged entry) for three reasons:

1. **Order guarantee**: the guard must run before any formatter can stage `.env` file
   contents.
2. **Distinct failure semantics**: a secrets-leak failure is an immediate abort, not a
   "fix and re-stage" lint error. Grouping it with formatters obscures the severity.
3. **Defense-in-depth**: a future lint-staged config change cannot silently weaken the
   secrets gate.

This is the single deliberate carve-out from the membership rule.

**Normative source**:
[tech-docs §5](../../../plans/done/2026-07-01__standardize-rhino-cli-sdlc-parity/tech-docs.md#5-nx-target-name-standard-targets-invoked-by-hooksci)

## Enforcement

The `validate:*` naming scheme is not validated at the Rust level (no clippy rule), but any
usage of the old form in `project.json` targets, `.husky/` hook files, `.github/workflows/`,
or `package.json` scripts is caught by the plan delivery gate:

```bash
grep -r "validate:" apps/*/project.json libs/*/project.json nx.json .husky/ .github/ package.json
```

A clean output (no matches) is the P10 / P11 gate criterion.

**See also**: [Nx Target Standards](./nx-targets.md) for the full required target set per
project type and caching rules, and [CI/CD Conventions](./ci-conventions.md) for the
Invariant E description.
