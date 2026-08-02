---
title: "SDLC Gate Registry Enforcement"
description: Make the ratified Gate Composition Rule mechanically enforced via a central gate registry, and retire main-ci.yml
category: explanation
subcategory: plans
tags:
  - ci-cd
  - git-hooks
  - governance
  - rhino-cli
  - parity
created: 2026-08-02
---

# SDLC Gate Registry Enforcement

**Status**: In Progress
**Delivery Mode**: `worktree-to-pr`
**Repos in scope**: `ose-public`, `ose-primer`, `ose-private`, `beaver-nest` (all four)

## The One-Sentence Problem

The repo already ratified the rule **`(pre-commit ∪ pre-push) == PR gate == main gate`** — same check
set, only the scope differs — in
[SDLC Gate Standard §Gate Composition Rule](../../../docs/reference/sdlc-gate-standard.md#gate-composition-rule),
but nothing enforces it, so the implementation has drifted away from the standard in **both
directions** in **all four repos**.

## Why This Plan Exists

This is **not** a design change. The target state is already normative. An audit on 2026-08-02 across
all four repos found the four gate surfaces no longer satisfy the rule they are documented to
satisfy. `[Repo-grounded]` — every row below was captured by reading each repo's actual `.husky/*`,
`package.json`, and `.github/workflows/*` files against the ratified standard; see
[tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today) for the full per-check
table this summarizes:

| Drift                                                                         | Evidence                                                                                                                                            |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Six checks are **pre-commit-only** — they never reach any CI gate             | `md naming validate`, `md frontmatter validate`, `convention emoji validate`, `docker compose config`, every formatter, `env staged-guard validate` |
| `harness bindings validate` is **pre-push-only** in all four repos            | Absent from `pr-quality-gate.yml` and `main-ci.yml`; `harness sync validate` / `npm run validate:sync` run in **zero** workflows                    |
| `md mermaid validate` + `md heading-hierarchy validate` are **main-ci-only**  | Absent from the PR gate in `ose-public`, `ose-primer`, `beaver-nest` (`ose-private` alone has them)                                                 |
| The PR gate's specs job is pinned to **one hardcoded project**                | `pr-quality-gate.yml` `specs-gate` runs `--projects=rhino-cli`; the standard says affected-scoped                                                   |
| Formatting is **never verified** anywhere, in any of **14** languages         | The PR `format` job auto-commits fixes rather than failing; `main-ci.yml` has no format job                                                         |
| Shell is linted but **never formatted** in two repos                          | `ose-primer` and `ose-private` run `shellcheck` with no `shfmt`; `ose-private` also formats terraform in a hook block, outside `lint-staged`        |
| **19 declared formatters match zero tracked files**                           | `ose-public` declares Go/Elixir/C#/Clojure/Dart formatters for languages it has none of; `beaver-nest` declares nine                                |
| The `rhino-cli` byte-identity boundary is **already violated**                | `src/application/agents/sync_validator.rs` differs between `ose-public` and the two other bound repos, under a **zero-carve-out** rule              |
| **No surface in any repo can detect** that violation                          | Byte-identity is a cross-repo property; every gate runs inside one repo. There is no manifest, no comparison, and no validator anywhere             |
| `beaver-nest`'s "fork" is mostly `ose-public`'s app names hardcoded in source | 8 of 9 divergences are repo-specific data (`STAGED_SKIP_PREFIXES`, `WEBSITE_APP_PREFIXES`, `.amazonq/cli-agents/ose-default.json`, test fixtures)   |
| ~700 lines of **dead** pre-commit pipeline replicated byte-for-byte           | `application/git/pre_commit.rs` is reachable only from `commands/git_pre_commit.rs`, which no CLI subcommand dispatches to                          |
| The PR gate's `format` job **does not run on push to `main`**                 | `if: github.event_name == 'pull_request'` — so a direct push to `main` skips the entire per-file validator set                                      |
| The standard's own Stage 3/4 tables omit checks that really run               | `md readme-index validate`, `harness duplication validate`, `convention license validate`                                                           |

The rule is right. The wiring is not. This plan makes the rule **impossible to violate** by moving the
check set out of hand-written shell and YAML into a single declared registry that both hooks and CI
read, plus a validator that fails when a surface silently drops a check.

## What Changes

1. **A gate registry** — a new `gates:` section in `repo-config.yml` declares **everything any
   surface does**, once: every pass/fail check (`type: check`) and every file-rewriting step
   (`type: mutation`), with its id, command, and scope **per surface**. Surfaces are `commit-msg`,
   `pre-commit`, `pre-push`, and `ci` — the four gate surfaces, and only those. This is the
   machine-readable promotion of the markdown SSOT that already exists in the SDLC Gate Standard —
   and because mutations are declared too, anything absent from `gates:` is run by no gate surface
   at all. Scheduled non-gating pipelines stay deliberately outside; see
   [tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).
2. **A rhino-cli `gate` command family** — `gate list` (enumerate; JSON feeds the CI matrix),
   `gate run --surface=<…>` (execute; used by the hooks), `gate emit` (regenerate the `lint-staged`
   block from the registry), and `gate validate` (the conformance gate: fails when a declared check
   is missing from a surface, a surface runs an undeclared check, or a generated artifact is stale).
   One supporting command, `git lockfile sync`, extracts the inline lockfile shell so it can be
   declared.
3. **`main-ci.yml` is deleted** in all four repos, after its unique checks are folded into the PR
   gate. The Gate Composition Rule is amended to `(pre-commit ∪ pre-push) == PR gate`.
4. **Four related findings closed** — `harness bindings validate` reaches CI, formatting gets a
   verify pass in **every** language rather than only prettier's, the stale `git-hook-lifecycle.md`
   is rewritten, and `deps-audit.yml` is replaced by `dependency-vulnerability-audit.yml` — kept out
   of the registry, but finally named for what it does (which needs a small
   workflow-naming-convention amendment to be legal).
5. **`rhino-cli` byte-identity becomes enforceable, across all four repos.** The same defect one
   layer down: a ratified zero-carve-out rule that nothing checks, and that is already broken. A
   committed checksum manifest turns local drift into a blocking gate; a scheduled audit compares
   manifests across repos. `apps/rhino-cli/tests/` joins the boundary. `beaver-nest` stops being a
   fork — which is possible only because its divergence was never a capability choice, but
   `ose-public`'s app names hardcoded into shared source. Extracting that data into `repo-config.yml`
   is the same move the registry already makes, which is why this rides here rather than in its own
   plan.

**Concrete target state is authored, not described.** [`repo-configs/`](./repo-configs/README.md),
[`husky-hooks/`](./husky-hooks/README.md), and [`package-json/`](./package-json/README.md) hold the
actual post-change files for each of the four repos. Execution copies from them, and the emitter is
correct when its output diffs clean against them.

## What Is Deliberately Lost

`main-ci.yml` is the only surface that ever runs `nx run-many --all`. Deleting it means **no surface
re-verifies the whole repo**. The PR gate's `push: [main]` trigger computes affected from
`github.event.before`, which covers the merged change itself but **not** cross-PR interaction: two PRs
that are individually green and mutually breaking will land on `main` with neither one's affected
graph covering the other.

This is an accepted, deliberate trade — recorded in [brd.md §Accepted Risk](./brd.md#accepted-risk)
with the mitigation options that were considered and declined.

## Delivery Units

Each unit is a delivery boundary — one worktree, one PR. See [delivery.md](./delivery.md) for the
full DAG and the per-phase gates.

| Phase | Unit                                                     | Repo          | Opens PR                  |
| ----- | -------------------------------------------------------- | ------------- | ------------------------- |
| 0     | Baseline convergence                                     | all four      | No (per the Phase-0 rule) |
| 1     | Gate engine — registry schema, `gate` commands, specs    | `ose-public`  | Yes                       |
| 1b    | De-fork canonical source + parity manifest               | `ose-public`  | Yes                       |
| 2     | Surface rewire + `main-ci.yml` deletion + doc amendments | `ose-public`  | Yes                       |
| 3     | Engine propagation + rewire                              | `ose-primer`  | Yes                       |
| 4     | Engine propagation + rewire                              | `ose-private` | Yes                       |
| 5     | Join the byte-identity boundary + rewire                 | `beaver-nest` | Yes                       |
| 6     | Knowledge capture                                        | `ose-public`  | Yes                       |

Phases 3, 4, and 5 are independent of one another and fan out up to the plan's concurrency cap.

**Phase 1b blocks every downstream phase.** The canonical source must be de-forked — dead pipeline
deleted, hardcoded app names extracted, `beaver-nest`'s `ROADMAP.md`/`SECURITY.md` exemptions
upstreamed — _before_ any repo copies it. Copying first would either recreate the fork or silently
delete capabilities `beaver-nest` depends on.

## Documents

- [brd.md](./brd.md) — why this matters, accepted risk, success definition
- [prd.md](./prd.md) — requirements and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — registry schema, command surface, conformance matrix, byte-identity design, doc amendments
- [delivery.md](./delivery.md) — phased, DAG-ordered execution checklist
- [learnings.md](./learnings.md) — knowledge capture (populated during execution)

Target-state artifacts, per repo. Each is a **complete file**, not a diff or an excerpt, so execution
copies rather than reconstructs:

- [repo-configs/](./repo-configs/README.md) — `repo-config-<repo>.yml`, the whole registry file
- [husky-hooks/](./husky-hooks/README.md) — `commit-msg-<repo>.sh`, `pre-commit-<repo>.sh`,
  `pre-push-<repo>.sh`, plus [`current/`](./husky-hooks/current/) holding the twelve hooks they
  replace, captured verbatim
- [package-json/](./package-json/README.md) — `package-<repo>.json`, the whole post-change file, plus
  `lint-staged-<repo>.json`, the block `gate emit` must produce

## Related

- [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md) — the normative rule this plan enforces
- [Git Hook Lifecycle](../../../repo-governance/development/workflow/git-hook-lifecycle.md) — stale; rewritten by this plan
- [Nx Targets](../../../repo-governance/development/infra/nx-targets.md) — references `main-ci.yml`
- [CI/CD System Architecture](../../../docs/reference/system-architecture/ci-cd.md) — references `main-ci.yml`
- [`2026-07-01__standardize-rhino-cli-sdlc-parity`](../../done/2026-07-01__standardize-rhino-cli-sdlc-parity/README.md) — the predecessor that ratified the rule
- [`tri-repo-rhino-cli-byte-identity-gate`](../../ideas/tri-repo-rhino-cli-byte-identity-gate.md) — the idea brief this plan fulfills: R-11/R-12's hermetic parity gate plus the scheduled unauthenticated-fetch audit ([tech-docs §2.8.4](./tech-docs.md#284-enforcement--a-hermetic-gate-plus-a-non-hermetic-audit)) answer its open questions on run location, cadence, and the `ose-private` auth model. Retired in Phase 6.
