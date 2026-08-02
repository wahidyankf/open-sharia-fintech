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
all four repos found the four gate surfaces no longer satisfy the rule they are documented to satisfy:

| Drift                                                                        | Evidence                                                                                                                                            |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Six checks are **pre-commit-only** — they never reach any CI gate            | `md naming validate`, `md frontmatter validate`, `convention emoji validate`, `docker compose config`, every formatter, `env staged-guard validate` |
| `harness bindings validate` is **pre-push-only** in all four repos           | Absent from `pr-quality-gate.yml` and `main-ci.yml`; `harness sync validate` / `npm run validate:sync` run in **zero** workflows                    |
| `md mermaid validate` + `md heading-hierarchy validate` are **main-ci-only** | Absent from the PR gate in `ose-public`, `ose-primer`, `beaver-nest` (`ose-private` alone has them)                                                 |
| The PR gate's specs job is pinned to **one hardcoded project**               | `pr-quality-gate.yml` `specs-gate` runs `--projects=rhino-cli`; the standard says affected-scoped                                                   |
| Formatting is **never verified** anywhere                                    | The PR `format` job auto-commits fixes rather than failing; `main-ci.yml` has no format job                                                         |
| The PR gate's `format` job **does not run on push to `main`**                | `if: github.event_name == 'pull_request'` — so a direct push to `main` skips the entire per-file validator set                                      |
| The standard's own Stage 3/4 tables omit checks that really run              | `md readme-index validate`, `harness duplication validate`, `convention license validate`                                                           |

The rule is right. The wiring is not. This plan makes the rule **impossible to violate** by moving the
check set out of hand-written shell and YAML into a single declared registry that both hooks and CI
read, plus a validator that fails when a surface silently drops a check.

## What Changes

1. **A gate registry** — a new `gates:` section in `repo-config.yml` declares every check once: its
   id, its command, and its scope **per surface**. This is the machine-readable promotion of the
   markdown SSOT that already exists in the SDLC Gate Standard.
2. **A rhino-cli `gate` command family** — `gate list` (enumerate, JSON for the CI matrix),
   `gate run --surface=<…>` (execute, used by the hooks), and `gate validate` (the conformance gate:
   fails when a declared check is missing from a surface, or a surface runs an undeclared check).
3. **`main-ci.yml` is deleted** in all four repos, after its unique checks are folded into the PR
   gate. The Gate Composition Rule is amended to `(pre-commit ∪ pre-push) == PR gate`.
4. **Four related findings closed** — `harness bindings validate` reaches CI, formatting gets a
   verify pass, the stale `git-hook-lifecycle.md` is rewritten, and `deps:audit` becomes a _declared_
   cron surface with a descriptive workflow name instead of an undeclared side-channel.

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
| 2     | Surface rewire + `main-ci.yml` deletion + doc amendments | `ose-public`  | Yes                       |
| 3     | Engine propagation + rewire                              | `ose-primer`  | Yes                       |
| 4     | Engine propagation + rewire                              | `ose-private` | Yes                       |
| 5     | Fork port + rewire                                       | `beaver-nest` | Yes                       |
| 6     | Knowledge capture                                        | `ose-public`  | Yes                       |

Phases 3, 4, and 5 are independent of one another and fan out up to the plan's concurrency cap.

## Documents

- [brd.md](./brd.md) — why this matters, accepted risk, success definition
- [prd.md](./prd.md) — requirements and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — registry schema, command surface, conformance matrix, doc amendments
- [delivery.md](./delivery.md) — phased, DAG-ordered execution checklist
- [learnings.md](./learnings.md) — knowledge capture (populated during execution)

## Related

- [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md) — the normative rule this plan enforces
- [Git Hook Lifecycle](../../../repo-governance/development/workflow/git-hook-lifecycle.md) — stale; rewritten by this plan
- [Nx Targets](../../../repo-governance/development/infra/nx-targets.md) — references `main-ci.yml`
- [CI/CD System Architecture](../../../docs/reference/system-architecture/ci-cd.md) — references `main-ci.yml`
- [`2026-07-01__standardize-rhino-cli-sdlc-parity`](../../done/2026-07-01__standardize-rhino-cli-sdlc-parity/README.md) — the predecessor that ratified the rule
