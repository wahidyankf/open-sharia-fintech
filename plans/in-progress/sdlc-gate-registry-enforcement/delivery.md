---
title: "Delivery — SDLC Gate Registry Enforcement"
description: Phased, DAG-ordered execution checklist with worktree specs, phase gates, and PR boundaries
category: explanation
subcategory: plans
tags:
  - ci-cd
  - delivery
  - parity
created: 2026-08-02
---

# Delivery — SDLC Gate Registry Enforcement

> **New-path legend**: `apps/rhino-cli/parity-manifest.sha256`,
> `.github/workflows/dependency-vulnerability-audit.yml`,
> `.github/workflows/rhino-cli-parity-audit.yml`, gate integration-test modules, and gate Gherkin
> feature files are **new files**. Every newly named selector in a RED task is a **new test**; task
> text repeats that marker at the production-behavior additions most likely to be mistaken as
> existing.

## Delivery Mode: worktree-to-pr

Each change-producing DAG leaf gets its own worktree and its own PR, strict 1-PR to 1-worktree. Every
PR runs the PR-Review Maker to Fixer Cycle (default three sequential CI-gated cycles) before merge.
`[AI]` merges by default.

**Target state is authored, not derived.** Phases 2 through 5 copy from
[`repo-configs/`](./repo-configs/README.md), [`husky-hooks/`](./husky-hooks/README.md), and
[`package-json/`](./package-json/README.md) and verify by diff. An acceptance clause reading "diffs
clean against the authored artifact" is falsifiable; "the registry is correct" is not.

## Worktree

Declared plan worktree path: `worktrees/sdlc-gate-registry-enforcement/`

This exact plan-slug path is the mandatory plan-execution worktree in `ose-public` and the first
delivery worktree in each sibling repo. Worktrees land under `worktrees/` in the repo root per the
[Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md), routed
there by the repo-local `WorktreeCreate` hook. Because `ose-public` has four distinct PR delivery
units, its later units use plan-slug suffixes to preserve strict 1-PR to 1-worktree ownership. The
same exact plan-slug path may exist independently in different repository roots.

| Phase | Worktree                                                  | Branch                                     | Repo                        |
| ----- | --------------------------------------------------------- | ------------------------------------------ | --------------------------- |
| 0     | `worktrees/sdlc-gate-registry-enforcement/`               | `sdlc-gate-registry-enforcement`           | `ose-public`                |
| 0     | none (primary checkout)                                   | `main`                                     | `ose-primer`, `ose-private` |
| 0     | `worktrees/gate-baseline-beaver/`                         | `main`                                     | `beaver-nest`               |
| 1     | `worktrees/sdlc-gate-registry-enforcement/`               | `sdlc-gate-registry-enforcement`           | `ose-public`                |
| 11    | `worktrees/sdlc-gate-registry-enforcement-defork/`        | `sdlc-gate-registry-enforcement-defork`    | `ose-public`                |
| 2     | `worktrees/sdlc-gate-registry-enforcement-rewire-public/` | `sdlc-gate-registry-enforcement-rewire`    | `ose-public`                |
| 3     | `worktrees/sdlc-gate-registry-enforcement/`               | `sdlc-gate-registry-enforcement`           | `ose-primer`                |
| 4     | `worktrees/sdlc-gate-registry-enforcement/`               | `sdlc-gate-registry-enforcement`           | `ose-private`               |
| 5     | `worktrees/sdlc-gate-registry-enforcement/`               | `sdlc-gate-registry-enforcement`           | `beaver-nest`               |
| 6     | `worktrees/sdlc-gate-registry-enforcement-knowledge/`     | `sdlc-gate-registry-enforcement-knowledge` | `ose-public`                |

`ose-public` and `beaver-nest` repository roots are intentionally bare, so commands requiring a
working tree cannot run there. Phase 0 uses the already-declared attached `ose-public` execution
worktree and creates `gate-baseline-beaver` from local `main`, records the baseline, then removes
only that task-owned Beaver worktree. Ref-level commands continue to run from the bare roots. Phase
5 likewise updates local `main` at the ref level after merge rather than trying to check it out in a
bare root. During Phase 0, the plan-owned `delivery.md` execution evidence is the sole permitted
public-worktree modification; every baseline cleanliness assertion excludes that exact path.

Optional manual pre-provisioning of the mandatory plan worktree (run from the repo root):

```bash
claude --worktree sdlc-gate-registry-enforcement
```

After every `git worktree add`, run `npm install` and `npm run doctor -- --fix` before any other
command — see
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md).

Plan-document edits (this folder) are made on local `main` under the plan-docs-only carve-out;
execution-time tick marks go in the worktree copy.

## Parallelization Model

Chosen capacity is **N=3 background agents plus one main-thread orchestrator**, the repository
default. The main thread owns the live task list, file-touch ledgers, dependency gates, and merges;
it does not take an implementation leaf while independent background work is available.

The serial spine is `Phase 0 → Phase 1 → Phase 11 → Phase 2`. Each node reads the source of truth
written by its predecessor. After Phase 2 merges, Phases 3, 4, and 5 are mutually independent because
they write different repositories while reading the same merged canonical engine and finalized
governance documents; they fan out concurrently up to N=3. Phase 6 is blocked by Phases 3, 4, and 5.
Cleanup is the terminal node, blocked by every delivery, merge, archival, and knowledge-capture node;
it removes only task-owned worktrees after explicit user confirmation and cannot run while another
node may still need them.

Dependency edges:

- `P0 blocks P1`.
- `P1 blocks P1b`.
- `P1b blocks P2`.
- `P2 blocks P3`, `P4`, and `P5` because those nodes propagate Phase 2's finalized governance files.
- `P3`, `P4`, and `P5` each block `P6`; none blocks another.
- `P6 blocks cleanup`; cleanup has no outgoing edge.

### Delivery Boundaries

Each change-producing phase below is individually a delivery boundary — one PR and one reversible
integration checkpoint. Phases 1–5 participate in the bounded byte-identity propagation transaction
below; each integrated boundary is a controlled pause-safe checkpoint when its exact refs and next
node are recorded, but is never described as invariant-restored or safe for unrelated boundary work.
See [README.md §Delivery Units](./README.md#delivery-units) for the canonical table.

| Phase | Unit                                                     | Repo          | Opens PR                  |
| ----- | -------------------------------------------------------- | ------------- | ------------------------- |
| 0     | Baseline convergence                                     | all four      | No (per the Phase-0 rule) |
| 1     | Gate engine — registry schema, `gate` commands, specs    | `ose-public`  | yes                       |
| 11    | De-fork canonical source + parity manifest               | `ose-public`  | yes                       |
| 2     | Surface rewire + `main-ci.yml` deletion + doc amendments | `ose-public`  | yes                       |
| 3     | Engine propagation + rewire                              | `ose-primer`  | yes                       |
| 4     | Engine propagation + rewire                              | `ose-private` | yes                       |
| 5     | Join the byte-identity boundary + rewire                 | `beaver-nest` | yes                       |
| 6     | Knowledge capture                                        | `ose-public`  | yes                       |

Phases 3, 4, and 5 are independent of one another after Phase 2 and fan out up to N=3.

### Bounded Byte-Identity Propagation Transaction

Phase 1's first thematic commit amends `docs/reference/sdlc-gate-standard.md` with this protocol, so
the authorization and the first canonical byte change merge together; no unamended interval exists.

- The Phase 0 ledger locks canonical baseline `ose-public` plus downstream baselines
  `ose-primer@0b67746b2befa4cb8cdbd1ab8f22ba20b6251f69`,
  `ose-private@346209fc4e9e63a913e6ef62b5823c6ebea271cb`, and
  `beaver-nest@cd2ec0e4de3375cfaa159847b5dc40f4790b1d53`.
- The transaction opens only when Phase 1 merges the protocol plus canonical change. While open,
  only this plan's Phases 1b–5 may change a boundary path; unrelated `apps/rhino-cli` changes and
  claims of restored byte identity are blocked.
- Each canonical checkpoint records `git rev-parse HEAD`, regenerates the manifest deliberately,
  and immediately advances the next serial node. After Phase 2, downstream Phases 3–5 copy that
  exact canonical tree and may fan out because they have disjoint repository ownership.
- The open transaction is a bounded Pause Safety state only at a green integrated phase gate with
  the four exact refs and earliest incomplete node recorded. To resume, run
  `git -C /Users/wkf/ose-projects/ose-public rev-parse origin/main`,
  `git -C /Users/wkf/ose-projects/ose-primer rev-parse origin/main`,
  `git -C /Users/wkf/ose-projects/ose-private rev-parse origin/main`, and
  `git -C /Users/wkf/ose-projects/beaver-nest rev-parse origin/main`; compare all four values with
  the transaction ledger, then continue the earliest incomplete node. Do not begin unrelated
  boundary work or claim restored identity while the transaction remains open.
- The transaction closes only after manifests and bounded byte diffs are identical at all four
  merged `origin/main` refs. Phase 6 is blocked until closure. If any downstream integration cannot
  converge, revert the Phase 1–2 canonical transaction commits rather than leave a permanent
  carve-out.

- [ ] [AI] **P1-PROPAGATION-PROTOCOL-RED** (`blocks: P1-PROPAGATION-PROTOCOL-GREEN`) — add a failing
      documentation assertion to `apps/rhino-cli/tests/docs.rs` named
      `byte_identity_window_requires_transaction_protocol` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test docs byte_identity_window_requires_transaction_protocol`
      — acceptance: fails because the standard does not define every open/close/block/revert rule.
- [ ] [AI] **P1-PROPAGATION-PROTOCOL-GREEN** (`blockedBy: P1-PROPAGATION-PROTOCOL-RED`; `blocks: P1-PROPAGATION-PROTOCOL-REFACTOR`) —
      add the exact protocol to `docs/reference/sdlc-gate-standard.md`. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test docs byte_identity_window_requires_transaction_protocol`
      — acceptance: exits 0 and the governing rule is amended before the first merge boundary.
- [ ] [AI] **P1-PROPAGATION-PROTOCOL-REFACTOR** (`blockedBy: P1-PROPAGATION-PROTOCOL-GREEN`; `blocks: P1-ENGINE`) —
      link the standard from `docs/reference/related-repositories.md`. Run
      `npm run lint:md` — acceptance: exits 0 and no prose calls an open transaction invariant-restored.

### Delivery-Boundary Quality and Commit Protocol

Every change-producing boundary runs these rules before its push task; phase-specific Land sections
repeat the exact branch and commit commands so they remain independently executable.

- [ ] [AI] **QUALITY-AFFECTED** — from the owning delivery worktree run
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: exits 0 for
      the complete affected blast radius. **Fix all failures, not just those caused by your
      changes.** Re-run this exact command after every repair until green.
- [ ] [AI] **QUALITY-SPLIT** — inspect the boundary ledger with
      `git diff --name-only --cached` — acceptance: each commit groups one theme/domain/concern;
      unrelated fixes are split rather than bundled.
- [ ] [AI] **QUALITY-COMMITS** — every commit uses
      `git commit -m '{type}({scope}): {imperative description}'` with no terminal period —
      acceptance: commitlint exits 0 and each Land section substitutes its exact message for this
      documented format.

The affected command is mandatory immediately before each push, not replaced by a narrower crate,
Markdown, or baseline command. A failure blocks push, review, merge readiness, and the next phase.

---

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification checklist
> plus a **Pause Safety** note (the safe-to-stop state after the phase and the single command to
> resume). A phase is **not complete until its gate is green**; do not start phase N+1 while any
> check in phase N's gate is failing.
>
> **Command shorthand** — a leading `...` at the **start of a command**, always followed by `--`,
> stands for `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml` (or the
> installed `rhino-cli` binary once Phase 1 ships it), so `... -- gate validate` means
> `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate`. This
> substitution applies **only** in that position. Elsewhere `...` keeps its ordinary meaning: git's
> triple-dot range operator in `HEAD...origin/main`, and elision in quoted excerpts.

---

## Phase 0 — Baseline Convergence

**Opens no PR.** Phase 0 evidence rides the Phase 1 PR.

- [x] [AI] Create `beaver-nest`'s baseline worktree from its bare root — command:
      `git -C /Users/wkf/ose-projects/beaver-nest worktree add worktrees/gate-baseline-beaver main` — acceptance:
      `git -C /Users/wkf/ose-projects/beaver-nest/worktrees/gate-baseline-beaver status --short --branch` reports
      a clean `main` level with `origin/main`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md` (execution evidence)
  - Notes: Created the task-owned Beaver baseline worktree; it is clean on `main` and `HEAD...origin/main` is `0 0`.

- [x] [AI] **P0-PUBLIC-INSTALL** (`blocks: P0-PUBLIC-DOCTOR`) — command:
      `npm --prefix /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement install`
      — acceptance: exits 0 in the declared attached public worktree; never run it in the bare root.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (dependency installation only)
  - Notes: Worktree-scoped installation exited 0; postinstall doctor completed.

- [x] [AI] **P0-PUBLIC-DOCTOR** (`blockedBy: P0-PUBLIC-INSTALL`) — command:
      `(cd /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement && npm run doctor -- --fix)`
      — acceptance: exits 0 and a check-only rerun reports no missing tool.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (toolchain setup only)
  - Notes: Doctor setup and check-only verification reported 16/16 tools OK with no warnings or missing tools; target sharing was initialized for four crates.

- [x] [AI] **P0-PRIMER-INSTALL** (`blocks: P0-PRIMER-DOCTOR`) — command:
      `npm --prefix /Users/wkf/ose-projects/ose-primer install` — acceptance: exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (dependency installation only)
  - Notes: Installation exited 0. Its postinstall doctor found no missing tools; it reported the pre-existing npm `11.11.0` versus `11.10.1` version warning.

- [x] [AI] **P0-PRIMER-DOCTOR** (`blockedBy: P0-PRIMER-INSTALL`) — command:
      `(cd /Users/wkf/ose-projects/ose-primer && npm run doctor -- --fix)` — acceptance: exits 0 and
      a check-only rerun reports no missing tool.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (toolchain setup only)
  - Notes: `npm run doctor -- --fix` repaired the Volta npm selection; the check-only rerun reported 13/13 tools OK with no warnings or missing tools.

- [x] [AI] **P0-PRIVATE-INSTALL** (`blocks: P0-PRIVATE-DOCTOR`) — command:
      `npm --prefix /Users/wkf/ose-projects/ose-private install` — acceptance: exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (dependency installation and local build only)
  - Notes: Installation exited 0. Its postinstall doctor found no missing tools and reported the pre-existing npm `11.11.0` versus required `11.16.0` version warning.

- [x] [AI] **P0-PRIVATE-DOCTOR** (`blockedBy: P0-PRIVATE-INSTALL`) — command:
      `(cd /Users/wkf/ose-projects/ose-private && npm run doctor -- --fix)` — acceptance: exits 0 and
      a check-only rerun reports no missing tool.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (toolchain setup only)
  - Notes: The fix and check-only doctor runs both reported 16/16 tools OK with no warnings or missing tools. Nx also emitted its non-blocking AI-agent configuration update notice.

- [x] [AI] **P0-BEAVER-INSTALL** (`blocks: P0-BEAVER-DOCTOR`) — command:
      `npm --prefix /Users/wkf/ose-projects/beaver-nest/worktrees/gate-baseline-beaver install` —
      acceptance: exits 0; never run it in the bare root.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (dependency installation only)
  - Notes: Installation in the attached task-owned worktree exited 0; postinstall doctor completed.

- [x] [AI] **P0-BEAVER-DOCTOR** (`blockedBy: P0-BEAVER-INSTALL`) — command:
      `(cd /Users/wkf/ose-projects/beaver-nest/worktrees/gate-baseline-beaver && npm run doctor -- --fix)`
      — acceptance: exits 0 and a check-only rerun reports no missing tool.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (toolchain setup only)
  - Notes: Doctor setup and check-only verification reported 16/16 tools OK with no warnings or missing tools; target sharing was initialized for two crates.

- [x] [AI] Establish a green baseline in `ose-public`: `(cd /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement && npx nx run-many --all -t test:quick)` —
      acceptance: exits 0. If any project fails, fix it before Phase 1 (preexisting failures are in
      scope per Root Cause Orientation); record each fix in this checklist as a discovered task.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (baseline validation only)
  - Notes: `npx nx run-many --all -t test:quick` exited 0 for the public execution worktree.

- [x] [AI] Confirm every working checkout is clean and level with origin: use the declared attached
      `ose-public` worktree, the `ose-primer` and `ose-private` primary checkouts, plus the
      `beaver-nest` baseline worktree. In the public worktree,
      `git status --porcelain -- . ':(exclude)plans/in-progress/sdlc-gate-registry-enforcement/delivery.md'`
      produces no output and `git merge-base --is-ancestor origin/main HEAD` succeeds; this permits
      only the plan-owned committed execution evidence to be ahead of trunk. In the other three,
      `git status --porcelain` produces no output and `git rev-list --left-right --count
HEAD...origin/main` reports `0 0` — acceptance: every checkout is clean outside plan-owned
      evidence and based on current trunk. If another path is dirty, the uncommitted work belongs to
      another actor: leave it untouched and record it here rather than staging it.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `delivery.md` (execution evidence)
  - Notes: The public worktree had no changes outside plan-owned execution evidence and contains current `origin/main`; primer, private, and Beaver baseline worktree were clean and each reported `0 0`.

- [x] [AI] Re-capture the audit table in [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today)
      against current `main` in all four repos — acceptance: every row's verdict still holds, or the
      table is amended in the same commit with the row that changed and why.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (audit validation only)
  - Notes: Re-fetched all four `origin/main` refs and diffed the audited hook, package, workflow, and repo-config paths against the recorded baselines. Primer, private, and Beaver have no relevant path changes; public only added two unrelated website local-deploy workflows. Every §1 gate-surface verdict remains current.

- [x] [AI] Record public branch protection — command: `gh api repos/wahidyankf/ose-public/branches/main/protection --jq '.required_status_checks.contexts'` — acceptance: context list or explicit API result is recorded.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (GitHub configuration observation only)
  - Notes: GitHub returned required contexts `["Quality gate"]`, unchanged from the recorded readiness baseline.

- [x] [AI] Record primer branch protection — command: `gh api repos/wahidyankf/ose-primer/branches/main/protection --jq '.required_status_checks.contexts'` — acceptance: context list or explicit API result is recorded.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (GitHub configuration observation only)
  - Notes: GitHub returned `Branch not protected` (HTTP 404), unchanged from the recorded readiness baseline.

- [x] [AI] Record private branch protection — command: `gh api repos/wahidyankf/ose-private/branches/main/protection --jq '.required_status_checks.contexts'` — acceptance: context list or explicit API result is recorded.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (GitHub configuration observation only)
  - Notes: GitHub returned branch-protection unavailable for this private repository (HTTP 403), unchanged from the recorded readiness baseline.

- [x] [AI] Record beaver branch protection — command: `gh api repos/wahidyankf/beaver-nest/branches/main/protection --jq '.required_status_checks.contexts'` — acceptance: context list or explicit API result is recorded.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (GitHub configuration observation only)
  - Notes: GitHub returned `Branch not protected` (HTTP 404), unchanged from the recorded readiness baseline.

`[Repo-grounded]` The 2026-08-04 refresh returned `["Quality gate"]` for `ose-public`, 404 for
`ose-primer` and `beaver-nest`, and 403 for `ose-private`. Phase 6 verifies the configured state is
unchanged; no repository-settings change is expected.

- [x] [AI] Record the byte-identity baseline across all four repos — acceptance: `diff -rq` output
      over `apps/rhino-cli/{src,tests}` and the gherkin tree is written into this checklist for every
      pair. The 2026-08-04 refresh found `sync_validator.rs` as the only three-repo difference and,
      relative to `ose-public`, ten source differences, four integration-test differences, three
      Gherkin differences, and a `project.json` difference in `beaver-nest`; re-verify rather than
      assume, since these repos are edited concurrently by other actors.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `delivery.md` (execution evidence)
  - Notes: `diff -rq` baseline recorded: public–primer `src=7 tests=2 gherkin=0`; public–private `src=7 tests=2 gherkin=0`; public–Beaver `src=15 tests=4 gherkin=3`; primer–private `src=0 tests=0 gherkin=0`; primer–Beaver `src=11 tests=6 gherkin=3`; private–Beaver `src=11 tests=6 gherkin=3`. Public differs from the identical primer/private pair in `sync_validator`, `target_share`, repo-config/audit orchestration, specs coverage, and Git root/staged-file paths. Beaver has the additional source/test/Gherkin divergences listed in P0-DRIFT-PRESERVATION.

- [x] [AI] **P0-DRIFT-PRESERVATION** (`blocks: P1`) — classify every newly observed Rhino source,
      test, and Gherkin divergence before canonical copying; upstream each required capability or
      explicitly prove it obsolete — acceptance: no Phase 1, 11, 3, 4, or 5 copy/overwrite can
      discard a currently unique behavior, and the final Phase 11 scope names every retained change.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `delivery.md`, `tech-docs.md`
  - Notes: Classification preserves Beaver's F# wrapper scanner/framework-key exclusion, naming exemptions, and inherited-Git test isolation; preserves public's later scope-correct Git-state handling, `CwdLock`, and serial test layout; extracts repository-specific Amazon-Q/frontmatter/fixture data; deletes the dead pipeline; and normalizes the equivalent sync-validator mismatch fixture. The Phase 11 canonical-preservation task and §2.8.5 now require the safe composition before any copy.

- [x] [AI] Record the tracked-file counts per language per repo that drive formatter pruning —
      `git ls-files` by extension — acceptance: the counts in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) still hold, or
      the table is amended in the same commit. A language gaining its first file changes which
      formatters a repo must declare.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `tech-docs.md`, `delivery.md`
  - Notes: Recounted all listed extensions in all four repositories. The table now records the live totals; public Go (230), Elixir (188), C# (199), and Dart (4) are tracked course-content artifacts and require retained formatter/verifier pairs. The follow-on P0-PUBLIC-CONTENT-FORMATTERS task updates the public target artifacts accordingly.

- [x] [AI] **P0-PUBLIC-CONTENT-FORMATTERS** (`blocks: P1`) — update the authored public registry,
      package, hook, and target artifacts for tracked Go, Elixir, C#, and Dart course-content files;
      preserve existing formatting behavior while adding a paired non-mutating verifier for every
      retained formatter — acceptance: all four formatter/verify pairs appear in the public target
      registry and emitted `lint-staged` block, and target artifacts remain complete-file JSON/YAML.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `repo-configs/repo-config-ose-public.yml`, `repo-configs/README.md`, `package-json/package-ose-public.json`, `package-json/lint-staged-ose-public.json`, `package-json/README.md`, `tech-docs.md`, `delivery.md`
  - Notes: Parsed target YAML/JSON successfully: the registry has 13 formatter mutations with unique IDs; Go, Elixir, C#, and Dart each have an exactly paired verifier; the 25-key emitted block exactly matches the complete package target; and the dead Clojure key is absent. The generated pre-commit hook remains intentionally unchanged because it delegates every declared formatter through `gate run` and `lint-staged`.

- [x] [AI] **P0-DOTNET-FANTOMAS-REPAIR** (`blocks: P1`) — diagnose and repair the public worktree's
      Fantomas runtime discovery, then rerun the affected F# lint targets and the all-project quick
      gate — acceptance: `dotnet tool restore && dotnet tool run fantomas --check
libs/fsharp-crane-core/src`, `dotnet tool restore && dotnet tool run fantomas --check
apps/ose-be/src`, `dotnet tool restore && dotnet tool run fantomas --check
apps/organiclever-be/src`, and
      `npx nx run-many --all -t test:quick` each exit 0 without suppressing a linter failure.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/crane-cli/project.json`, `apps/ose-be/project.json`, `apps/organiclever-be/project.json`, `libs/fsharp-crane-core/project.json`, `delivery.md`
  - Notes: RED: every bare global `fantomas --check` failed because its app host received no runtime root. GREEN: all F# lint targets now restore and invoke the pinned local manifest tool using `dotnet tool restore && dotnet tool run fantomas --check`; `npx nx run-many --all -t test:quick` then exited 0 for all 29 projects and dependencies. The fix retains actual formatting failures as non-zero exits.

- [x] [AI] **P0-DOTNET-FANTOMAS-REGRESSION-RED** (`blocks: P0-DOTNET-FANTOMAS-REGRESSION-GREEN`) —
      reproduce the runtime-discovery failure with the prior bare global Fantomas command and add a
      check-mode scenario using a deliberately unformatted temporary F# fixture — acceptance: the
      pre-repair target command exits non-zero and the fixture makes manifest Fantomas exit non-zero.
      File: `apps/rhino-cli/tests/fsharp_tool_invocation.rs`. Command:
      `fantomas --check libs/fsharp-crane-core/src` — acceptance: exits non-zero before the repair
      because the global app host cannot discover its runtime.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/fsharp_tool_invocation.rs`, `specs/apps/rhino/behavior/rhino-cli/gherkin/system/fsharp-tool-invocation.feature`
  - Notes: The pre-repair global command failed with exit 131 because its app host could not discover .NET. The new scenario creates an unformatted temporary `.fs` fixture; manifest Fantomas reports it needs formatting and exits non-zero.

- [x] [AI] **P0-DOTNET-FANTOMAS-REGRESSION-GREEN** (`blockedBy: P0-DOTNET-FANTOMAS-REGRESSION-RED`; `blocks: P0-DOTNET-FANTOMAS-REGRESSION-REFACTOR`) —
      wire the Cucumber harness into Rhino's unit target and assert all four F# lint targets use the
      restored local manifest tool — acceptance: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test fsharp_tool_invocation` exits 0 while observing the fixture's expected non-zero check.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/Cargo.toml`, `apps/rhino-cli/project.json`, `apps/rhino-cli/tests/fsharp_tool_invocation.rs`, `specs/apps/rhino/behavior/rhino-cli/gherkin/system/README.md`
  - Notes: The `harness = false` target executes one Cucumber scenario and five steps rather than silently reporting zero tests; all passed while emitting the expected `needs formatting` fixture result.

- [x] [AI] **P0-DOTNET-FANTOMAS-REGRESSION-REFACTOR** (`blockedBy: P0-DOTNET-FANTOMAS-REGRESSION-GREEN`; `blocks: P1`) —
      keep the fixture temporary, preserve strict formatter exit behavior, and verify formatting,
      Clippy, and behavior-spec coverage — acceptance: `cargo fmt --check`,
      `cargo clippy --all-targets -- -D warnings`, and `npx nx run rhino-cli:specs:behavior:coverage`
      each exit 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `tech-docs.md`, `delivery.md`
  - Notes: All three validation commands passed; behavior coverage reports 61 specs, 374 scenarios, and 1,557 covered steps. The fixture lives in the system temp directory and is automatically removed.

- [x] [AI] Remove only the task-owned `beaver-nest` baseline worktree after all Phase 0 evidence is
      captured — command:
      `git -C /Users/wkf/ose-projects/beaver-nest worktree remove worktrees/gate-baseline-beaver && git -C /Users/wkf/ose-projects/beaver-nest worktree prune`
      — acceptance: `git -C /Users/wkf/ose-projects/beaver-nest worktree list --porcelain` contains no
      `gate-baseline-beaver`, while unrelated worktrees remain untouched, and
      `git -C /Users/wkf/ose-projects/beaver-nest rev-list --left-right --count main...origin/main` reports `0 0`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (worktree cleanup only)
  - Notes: Verified the exact path was a clean `main` worktree at `cd2ec0e4`, removed only that path, pruned stale records, and confirmed `git worktree list --porcelain` now reports solely the bare repository root.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npx nx run-many --all -t test:quick` exits 0 in `ose-public` — green baseline
      established.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: After the manifest-based Fantomas repair, the complete command exited 0 for all 29 projects and 13 dependent targets; 41 of 42 tasks were valid cache hits on the final rerun.

- [x] [AI] `git status --porcelain` is empty and
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0` in the three primary
      checkouts; the captured `beaver-nest` baseline showed the same before removal, and its bare-root
      `main...origin/main` ref comparison still reports `0 0`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: Primer and private primary worktrees remain clean and each reports `0 0`; Beaver's bare-root `main...origin/main` reports `0 0` after the task-owned baseline worktree removal.

- [x] [AI] [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today)'s audit table
      re-verified against current `main` in all four repos — every row's verdict still holds, or the
      table is amended in the same commit.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: The current-main comparison was captured after fetching all four origins; every audited gate-surface verdict remains current, with only unrelated public website local-deploy workflows added.

- [x] [AI] Branch-protection required-status-check names recorded for each repo (written into this
      checklist).
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (GitHub configuration observation only)
  - Notes: Recorded `ose-public` required context `Quality gate`; Primer and Beaver returned HTTP 404 (not protected); private returned HTTP 403 (unavailable to the current token). Each result is preserved in the Phase 0 task evidence.

- [x] [AI] Byte-identity baseline captured across all four repos (`diff -rq` output recorded into
      this checklist).
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: Every pairwise source, test, and Gherkin boundary count is recorded in the baseline task; P0-DRIFT-PRESERVATION classifies every non-identical path before canonical copying can begin.

- [x] [AI] Per-language tracked-file counts confirmed against
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory).
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: Live counts amend §2.2.4, including public course-content Go, Elixir, C#, and Dart files; target formatter coverage now retains their four pairs and removes only untracked Clojure.

- [x] [AI] The task-owned `beaver-nest` baseline worktree is removed and unrelated worktrees are
      unchanged.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: The exact baseline path is absent after `git worktree remove` and prune; `beaver-nest` reports only its bare root, so no unrelated attached worktree was removed.

> **Pause Safety**: the three primary checkouts are clean; `beaver-nest`'s local `main` ref is level
> with `origin/main`; and all four repos' baseline state
> (audit table, branch-protection contexts, byte-identity diff, per-language counts) is recorded in
> this checklist. The task-owned baseline worktree is removed. Safe to stop. To resume: run
> `git status --porcelain` in the three primary checkouts and compare `main...origin/main` in the
> `beaver-nest` bare root, then start Phase 1.

---

## Phase 1 — Gate Engine (`ose-public`, PR #1)

Delivery unit: the registry schema and the `gate` command family, with nothing wired to it yet. The
engine ships inert — no hook or workflow changes — and is reversible as a transaction checkpoint.
Its merge opens the bounded propagation transaction; it is not an invariant-restored pause point.

Every code step below uses the RED / GREEN / REFACTOR template.

- [x] [AI] Enter the pre-provisioned declared worktree or create it from fresh `origin/main` —
      commands: `git fetch origin main` and, only when the declared worktree does not already
      exist, `git worktree add -b sdlc-gate-registry-enforcement worktrees/sdlc-gate-registry-enforcement origin/main`
      — acceptance: `git -C worktrees/sdlc-gate-registry-enforcement status --short --branch` is
      clean and `git -C worktrees/sdlc-gate-registry-enforcement merge-base --is-ancestor origin/main HEAD`
      succeeds. A resumed execution branch may be ahead of `origin/main` only by its committed,
      plan-owned Phase 0 evidence; enumerate `origin/main..HEAD` and verify that every commit is
      recorded by the Phase 0 checklist before continuing. A freshly provisioned worktree instead
      reports `0 0` for `git rev-list --left-right --count HEAD...origin/main`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md` (resumed-worktree contract)
  - Notes: Fetched `origin/main`; the declared worktree is clean, contains current trunk, and is nine commits ahead solely for recorded plan-validation, Phase 0 evidence, and the Phase 0 Fantomas regression repair. `git merge-base --is-ancestor origin/main HEAD` exits 0; the strict detached plan check is clean (report `plan__439846__2026-08-04--16-01__audit.md`).
- [x] [AI] Install the Phase 1 worktree dependencies — command:
      `npm --prefix worktrees/sdlc-gate-registry-enforcement install` — acceptance: exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (dependency installation only)
  - Notes: Installation exited 0 in the declared worktree; its postinstall doctor confirmed all 16 required tools, no warnings, and no missing tools.
- [x] [AI] Initialize the Phase 1 worktree toolchain — command:
      `(cd worktrees/sdlc-gate-registry-enforcement && npm run doctor -- --fix)` — acceptance: exits
      0 and a subsequent doctor run reports no missing tool.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (toolchain setup only)
  - Notes: `npm run doctor -- --fix` found nothing to repair; the following check-only doctor run reported 16/16 tools OK, zero warnings, and zero missing tools.

### 1.1 Registry schema in `repo-config.yml`

- [x] [AI] **RED** — add a failing test at
      `apps/rhino-cli/tests/repo_config_data_driven.rs` asserting that a `gates:` section
      deserializes into a `Vec<GateEntry>` with `id`, `type`, `command`, `kind`, `surfaces` —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven`
      — acceptance: fails with a missing-field or unknown-variant error naming `gates`. Confirm it
      fails _for that reason_, not a compile error unrelated to the new field.

  **Gherkin (underpins) →** "A check declares a different scope per surface"; "Every surface step is
  declared, whatever its type"; "An unknown scope value is rejected at parse time"; "A duplicate gate
  id is rejected"; "An unknown type value is rejected at parse time"; "A mutation may not declare a
  wiring value"
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Added a synthetic `gates:` fixture carrying `id`, `type`, `command`, `kind`, and per-surface `scope`. The exact test command exits 101 because strict deserialization reports `unknown field gates`; that is the intended missing-model failure.

- [x] [AI] **GREEN** — add the `gates` field and the `GateEntry` / `SurfaceScope` types to the
      `repo-config` domain model, per the field contract in
      [tech-docs §2.2](./tech-docs.md#22-registry-location-and-shape) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` —
      acceptance: exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/application/repo_config/mod.rs`
  - Notes: Added the `gates` registry field plus deserializable gate and per-surface scope models. The RED fixture now deserializes and the exact integration test exits 0.
- [x] [AI] **REFACTOR** — enum values for `type`, `kind`, `wiring`, `carve-out`, surface name, and
      `scope` are `#[serde(rename_all)]` strict variants with deny-unknown-fields, so a typo fails
      rather than defaulting — acceptance: a test asserting `scope: sometimes` is rejected exits 0,
      and the rejection message names the allowed values. Same for `type: cleanup`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/application/repo_config/mod.rs`, `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Replaced permissive registry strings with strict serde enums and deny-unknown-fields gate/scope records. The focused integration test rejects both invalid values while naming the accepted vocabulary; the repo-config library suite reports 18 passing tests.
- [x] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/repo_config_data_driven.rs`: a
      `wiring` value declared on `type: mutation` is rejected (`wiring` is valid only on
      `type: check`) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` —
      acceptance: fails because the applicability check does not exist yet.

  **Gherkin (binds) →** "A mutation may not declare a wiring value"

  ```gherkin
  Scenario: A mutation may not declare a wiring value
    Given a gate declares type "mutation" and wiring "matrix"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message states that wiring applies to checks only
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Added a schema-valid mutation fixture with `wiring: matrix` and invoked the real `repo-config validate` path. The focused test exits 101 because the command wrongly reports the config valid, isolating the absent applicability rule.

- [x] [AI] **GREEN** — implement field-applicability validation for `wiring` so the misapplication
      test asserts non-zero exit with a message naming the field and the type it does not apply to,
      and the inverse (correctly-applied `wiring`) exits 0 — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` — acceptance: the
      new test passes plus the correctly-applied case exits 0, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/repo_config_validate.rs`, `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: `repo-config validate` now rejects `gates[0].wiring` for `type mutation` while accepting `wiring: matrix` for a check. The data-driven integration test and eight focused validator unit tests pass.
- [x] [AI] **RED** — add two failing tests at `apps/rhino-cli/tests/repo_config_data_driven.rs` for
      the remaining field-applicability rules: `restages` declared on `type: check`, and `carve-out`
      declared on `type: mutation` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` —
      acceptance: both fail because the applicability check does not cover `restages`/`carve-out`
      yet.

  **Gherkin (binds) →** "A field applied to the wrong gate type is rejected"

  ```gherkin
  Scenario Outline: A field applied to the wrong gate type is rejected
    Given a gate declares type "<type>"
    And it carries the field "<field>"
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the gate id and the misapplied field

    Examples:
      | type     | field     |
      | check    | restages  |
      | mutation | carve-out |
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Added two schema-valid invalid-applicability fixtures and exercised the actual validator. The focused test exits 101 because both configurations incorrectly pass, isolating the two absent rules.

- [x] [AI] **GREEN** — extend field-applicability validation to `restages` (valid only on
      `type: mutation`) and `carve-out` (valid only on `type: check`), matching the message shape
      from the `wiring` case — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` — acceptance: both new tests pass plus the
      correctly-applied cases exit 0, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/repo_config_validate.rs`, `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: The validator now rejects `restages` on checks and `carve-out` on mutations, and the inverse legal configurations pass. The focused integration test and focused validator unit suite are green.
- [x] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/repo_config_data_driven.rs`:
      `rhino-cli repo-config validate` must reject a registry with duplicate gate ids — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` —
      acceptance: fails because `repo-config validate` does not yet reject duplicate ids.

  **Gherkin (binds) →** "A duplicate gate id is rejected"

  ```gherkin
  Scenario: A duplicate gate id is rejected
    Given repo-config.yml declares two gates both with id "md-links"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the duplicated id
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Added two schema-valid gates with the same identifier and ran the real validator. The focused test exits 101 because duplicate IDs still pass, isolating the required uniqueness validation.

- [x] [AI] **GREEN** — implement duplicate-id rejection in `rhino-cli repo-config validate`, the
      failure naming the offending id, and confirm the inverse (unique ids) exits 0 — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` —
      acceptance: the new test passes and the inverse case exits 0, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/repo_config_validate.rs`, `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: The validator now reports the second duplicate as `gates[1].id` and names its repeated value. The data-driven suite verifies rejection and a distinct-ID inverse; focused validator tests pass.
- [x] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/repo_config_data_driven.rs`:
      `rhino-cli repo-config validate` must reject a gate declaring an empty `surfaces` map —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven`
      — acceptance: fails because `repo-config validate` does not yet reject an empty `surfaces`
      map.

  **Gherkin (binds) →** "A gate declaring no surfaces at all is rejected"

  ```gherkin
  Scenario: A gate declaring no surfaces at all is rejected
    Given a gate declares an empty "surfaces" map
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the gate id
    And the message states that a gate must declare at least one surface
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: Added a schema-valid `surfaces: {}` fixture and invoked the real validator. The focused test exits 101 because it is accepted, isolating the required non-empty invariant.

- [x] [AI] **GREEN** — implement empty-`surfaces`-map rejection in `rhino-cli repo-config validate`,
      the failure naming the gate id and stating a gate must declare at least one surface, and
      confirm the inverse (non-empty surfaces) exits 0 — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` — acceptance: the new
      test passes and the inverse case exits 0, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/repo_config_validate.rs`, `apps/rhino-cli/tests/repo_config_data_driven.rs`
  - Notes: A gate with no surfaces now yields a message naming `no-surfaces` and requiring at least one surface; the non-empty inverse is covered. The data-driven integration and focused validator unit tests pass.

### 1.2 `gate list`

- [x] [AI] **RED** — failing test: `gate list --surface=ci --format=json` returns only the gates
      declaring the `ci` surface, each carrying `id`, `type`, `command`, `scope` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list` — acceptance: fails
      because the command does not exist.

  **Gherkin (binds) →** "JSON output drives a GitHub Actions matrix"

  ```gherkin
  Scenario: JSON output drives a GitHub Actions matrix
    Given the registry declares gates on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output is a JSON array
    And every element carries "id", "command", and "scope" keys
    And the array contains exactly the gates declaring surface "ci"
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands.rs`, `apps/rhino-cli/src/commands/gate/mod.rs`, `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: Added one real lib assertion with a synthetic registry containing two CI gates and one pre-commit-only gate. `cargo test --lib gate::list` runs that assertion and exits 101 because the command path is deliberately unimplemented, not because Cargo filtered it away.

- [x] [AI] **GREEN** — implement `gate list` and wire it into `cli.rs` — acceptance: same command
      exits 0; `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate list --surface=ci --format=json | jq -e 'type == "array"'`
      exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands.rs`, `apps/rhino-cli/src/commands/gate/mod.rs`, `apps/rhino-cli/src/commands/gate/list.rs`, `apps/rhino-cli/src/cli.rs`
  - Notes: Added `gate list` CLI dispatch, registry filtering by surface, and JSON projections with `id`, `type`, `command`, and `scope`. The focused test passes; the release command emits an empty JSON array against the current pre-rewire config and passes `jq` type validation.
- [x] [AI] **REFACTOR** — a valid surface with no declared gates returns `[]` and exit 0, while an
      unknown surface is rejected — acceptance: a synthetic registry with no `commit-msg` gates
      makes `... -- gate list --surface=commit-msg --format=json` print `[]` and exit 0;
      `... -- gate list --surface=cron --format=json` exits non-zero and names the four allowed
      surfaces.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: Focused gate-list tests cover all valid empty surfaces and reject `cron` while naming `commit-msg`, `pre-commit`, `pre-push`, and `ci`. The empty-surface JSON command passes its array contract.
- [x] [AI] **RED** — add a failing test in the `gate::list` module: `--format=json` must omit
      `wiring: hand-wired` gates (asserting `test-quick` is absent from
      `gate list --surface=ci --format=json`) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list::format_json_omits_hand_wired`
      — acceptance: fails because the `--format=json` path does not exclude hand-wired gates yet.

  **Gherkin (binds) →** "A hand-wired gate produces no matrix row"

  ```gherkin
  Scenario: A hand-wired gate produces no matrix row
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output contains no entry with id "test-quick"
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: Added a focused projection fixture with a matrix CI gate and hand-wired `test-quick`. The exact single-test command exits 101 because JSON currently includes the hand-wired entry.

- [x] [AI] **GREEN** — implement the `--format=json` projection so it excludes `wiring: hand-wired`
      gates — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list::format_json_omits_hand_wired`
      — acceptance: the new test passes, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: JSON matrix projection now omits hand-wired gates. The exact focused test and the full gate-list unit set (four tests) pass.
- [x] [AI] **RED** — add a failing test in the `gate::list` module: `--format=text` must still
      include `wiring: hand-wired` gates, each marked as hand-wired (asserting `test-quick` is
      present in `gate list --surface=ci --format=text` and flagged) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list::format_text_includes_hand_wired`
      — acceptance: fails because the `--format=text` path does not exist yet.

  **Gherkin (binds) →** "A hand-wired gate is still listed in text output"

  ```gherkin
  Scenario: A hand-wired gate is still listed in text output
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    When "rhino-cli gate list --surface=ci --format=text" runs
    Then the output contains an entry with id "test-quick"
    And that entry is marked as hand-wired
    # text output is for humans auditing completeness; json output feeds the
    # matrix, which must not double-run a job that already exists by hand.
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: Added a focused text-output assertion. It executes and exits 101 only because the otherwise listed hand-wired gate lacks its required marker.

- [x] [AI] **GREEN** — implement the `--format=text` projection so hand-wired gates are included and
      marked as hand-wired — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list::format_text_includes_hand_wired`
      — acceptance: the new test passes, no other tests
      broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/list.rs`
  - Notes: Human-readable list output now retains hand-wired gates and marks them, while JSON remains matrix-only. The exact test and five-test gate-list suite pass.

### 1.2a `git lockfile sync`

The lockfile-sync step is inline shell in `.husky/pre-commit` today and cannot be declared until it
is a real command. See [tech-docs §2.2.1](./tech-docs.md#221-why-mutations-are-in-the-registry).

- [x] [AI] **RED** — failing test: given a staged `apps/<x>/package.json` whose dependency change
      leaves `apps/<x>/package-lock.json` stale, the command regenerates and stages
      `apps/<x>/package-lock.json`, with both files landing in the same commit — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib git::lockfile::regenerates_when_stale`
      — acceptance: fails because the command does not exist.

  **Gherkin (binds) →** "lockfile-sync regenerates the lockfile and restages it"

  ```gherkin
  Scenario: lockfile-sync regenerates the lockfile and restages it
    Given a staged package.json changes a dependency
    And package-lock.json is stale with respect to it
    When the gate with id "lockfile-sync" runs on surface "pre-commit"
    Then package-lock.json is regenerated
    And the regenerated package-lock.json is staged
    And the commit proceeds with both files in the same commit
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands.rs`, `apps/rhino-cli/src/commands/git/mod.rs`, `apps/rhino-cli/src/commands/git/lockfile.rs`
  - Notes: Grounded the scenario in the existing hook’s staged-app and existing-lockfile behavior. The real filtered unit test stages a stale fixture and exits 101 solely because the command path is unimplemented.

- [x] [AI] **GREEN** — implement `rhino-cli git lockfile sync`, porting the hook's existing logic
      verbatim, so a stale lockfile is regenerated and staged alongside the staged `package.json` —
      command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib git::lockfile::regenerates_when_stale`
      — acceptance: the new test passes.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands.rs`, `apps/rhino-cli/src/commands/git/mod.rs`, `apps/rhino-cli/src/commands/git/lockfile.rs`, `apps/rhino-cli/src/cli.rs`
  - Notes: Implemented staged-app discovery, existing-lockfile guard, lockfile-only npm regeneration, and restaging. The stale-lockfile test passes alongside format and diff checks.
- [x] [AI] **RED** — failing test: given a staged `apps/<x>/package.json` whose
      `apps/<x>/package-lock.json` is already current, the command leaves the lockfile unchanged and
      stages nothing additional — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib git::lockfile::noop_when_current`
      — acceptance: fails because the command does not yet distinguish the already-current case from
      the stale case.

  **Gherkin (binds) →** "lockfile-sync is a no-op when the lockfile is already current"

  ```gherkin
  Scenario: lockfile-sync is a no-op when the lockfile is already current
    Given a staged package.json matches package-lock.json
    When the gate with id "lockfile-sync" runs on surface "pre-commit"
    Then package-lock.json is unchanged
    And nothing additional is staged
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/git/lockfile.rs`
  - Notes: Added an indexed current-lockfile fixture with matching package metadata. The exact filtered test exits 101 because the command still runs a sync action instead of no-oping.

- [x] [AI] **GREEN** — implement the already-current no-op path so a matching lockfile is left
      byte-unchanged and nothing extra is staged — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib git::lockfile::noop_when_current`
      — acceptance: the new test
      passes, no other tests broken.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/git/lockfile.rs`
  - Notes: The command compares lock-relevant manifest and root-lock metadata before invoking npm. Current files remain byte-identical and unstaged; stale lockfiles still regenerate. Both focused tests and formatter check pass.
- [x] [AI] **REFACTOR** — no-op cleanly when no `package.json` is staged at all (a third, distinct
      condition from the stale/current cases above) — acceptance: a test asserting exit 0 with no
      git index mutation passes.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/git/lockfile.rs`
  - Notes: No staged app manifest now returns success before any mutation. A staged README fixture confirms no output and unchanged index; all three lockfile cases pass.

### 1.2b `gate emit`

- [x] [AI] **RED** — failing test: `gate emit --surface=pre-commit` writes a `lint-staged` block
      matching the registry's per-file gates — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::emit` — acceptance: fails
      because the command does not exist.

  **Gherkin (binds) →** "The emitter reproduces the registry's per-file entries"

  ```gherkin
  Scenario: The emitter reproduces the registry's per-file entries
    Given the registry declares per-file gates on surface "pre-commit"
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the "lint-staged" block in package.json contains one glob key per declared glob
    And each key lists that glob's commands in declaration order
  ```

  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/mod.rs`, `apps/rhino-cli/src/commands/gate/emit.rs`
  - Notes: Added one real emitter assertion with two ordered markdown gates and an unrelated CI gate. The focused test exits 101 solely because the emitter path is not implemented.

- [x] [AI] **GREEN** — implement `gate emit --surface=pre-commit` — acceptance: same command exits 0.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/mod.rs`, `apps/rhino-cli/src/commands/gate/emit.rs`, `apps/rhino-cli/src/cli.rs`
  - Notes: Emission selects affected-file-type pre-commit gates, expands globs, preserves declaration order per glob, and replaces the lint-staged object. The focused test passes; Rust formatting and diff validation pass. Help is available when supplied with the required surface argument.
- [x] [AI] **REFACTOR** — the emitter is **marker-first**: it locates the already-applied marker
      before the anchor, so a re-run replaces rather than appends — acceptance: a test running the
      emitter twice asserts the second result is byte-identical to the first **and** that the block
      appears exactly once. A test that only checks byte-equality would pass on a duplicated block if
      both runs duplicated identically, so the occurrence count is required.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `apps/rhino-cli/src/commands/gate/emit.rs`
  - Notes: Existing `lint-staged` is now the marker and its value is replaced before insertion is considered. Two-emission coverage asserts both byte identity and exactly one generated key; the emitter suite passes.

### 1.3 `gate run`

- [ ] [AI] **RED** — failing test: gates declared for a surface are invoked in declaration order —
      command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::declaration_order` —
      acceptance: fails because the command does not exist.

  **Gherkin (binds) →** "Pre-push runs every gate declared for the pre-push surface"

  ```gherkin
  Scenario: Pre-push runs every gate declared for the pre-push surface
    Given the registry declares gates "md-links" and "env" on surface "pre-push"
    When "rhino-cli gate run --surface=pre-push" runs
    Then both gate commands are invoked
    And they are invoked in declaration order
  ```

- [ ] [AI] **GREEN** — implement `gate run --surface=<name>` so it invokes every gate declared for
      that surface, in declaration order — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::declaration_order` — acceptance: the new test passes.
- [ ] [AI] **RED** — add a failing test: execution stops at the first failing gate and the next
      declared gate is not invoked — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::stop_at_first_failure`
      — acceptance: fails because `gate run` does not yet stop at the first failure.

  **Gherkin (binds) →** "Execution stops at the first failing gate"

  ```gherkin
  Scenario: Execution stops at the first failing gate
    Given the registry declares gates "first" then "second" on surface "pre-push"
    And gate "first" fails
    When "rhino-cli gate run --surface=pre-push" runs
    Then it exits non-zero
    And gate "second" is not invoked
  ```

- [ ] [AI] **GREEN** — implement stop-at-first-failure — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::stop_at_first_failure`
      — acceptance: the new
      test passes, no other tests broken.
- [ ] [AI] **RED** — add a failing test: a `scope: path-gated` gate is skipped when its trigger
      paths do not intersect the changed set — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::path_gated_skip` —
      acceptance: fails because path-gating does not exist yet.

  **Gherkin (binds) →** "A path-gated check is skipped when its trigger path is untouched"

  ```gherkin
  Scenario: A path-gated check is skipped when its trigger path is untouched
    Given gate "harness-bindings" declares surface "pre-push" with scope "path-gated"
    And its trigger paths do not intersect the changed set
    When "rhino-cli gate run --surface=pre-push" runs
    Then gate "harness-bindings" is not invoked
    And the run exits zero
  ```

- [ ] [AI] **GREEN** — implement the path-gated skip path — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::path_gated_skip` — acceptance: the
      new test passes, no other tests broken.
- [ ] [AI] **RED** — add a failing test: a `scope: path-gated` gate is invoked when a file under
      its trigger paths is in the changed set — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::path_gated_run` —
      acceptance: fails because a path-gated gate is never invoked yet.

  **Gherkin (binds) →** "A path-gated check runs when its trigger path is touched"

  ```gherkin
  Scenario: A path-gated check runs when its trigger path is touched
    Given gate "harness-bindings" declares surface "pre-push" with scope "path-gated"
    And a file under ".claude/agents/" is in the changed set
    When "rhino-cli gate run --surface=pre-push" runs
    Then gate "harness-bindings" is invoked
  ```

- [ ] [AI] **GREEN** — implement the path-gated run path — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run::path_gated_run` — acceptance: the
      new test passes, no other tests broken.
- [ ] [AI] **REFACTOR** — resolve `repo-config.yml` and all exclude paths from
      `git rev-parse --show-toplevel`, never the main checkout; never call
      `git rev-parse --is-bare-repository` — acceptance: a regression test that runs `gate run` from a
      synthetic linked worktree exits 0 and reads the worktree's own config; and
      `grep -rn "is-bare-repository" apps/rhino-cli/src/` returns no match.

#### 1.3a Complete dispatch-contract TDD

All selectors below are **new tests** in `apps/rhino-cli/tests/gate_dispatch.rs` (**new file**).
Every cycle is bound to the matching R-3 Gherkin scenario in [prd.md](./prd.md#r-3--execution-from-the-hooks).

- [ ] [AI] **P1-DISPATCH-KIND-RHINO-RED** (`blocks: P1-DISPATCH-KIND-RHINO-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `rhino_cli_kind_receives_derived_files` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch rhino_cli_kind_receives_derived_files`
      — acceptance: fails because the `rhino-cli` kind does not yet append only its derived files
      or propagate the leaf exit code.

  **Gherkin (binds) →** "Rhino CLI kind receives derived files"

  ```gherkin
  Scenario: Rhino CLI kind receives derived files
    Given a rhino-cli gate matches staged files "a.md" and "b.md"
    When "rhino-cli gate run --surface=pre-commit --only=md-naming" runs
    Then the local rhino-cli leaf receives only "a.md" and "b.md" and its exit code is propagated
  ```

- [ ] [AI] **P1-DISPATCH-KIND-RHINO-GREEN** (`blockedBy: P1-DISPATCH-KIND-RHINO-RED`;
      `blocks: P1-DISPATCH-KIND-RHINO-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only `rhino-cli` kind derived-file argv and exit
      propagation. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch rhino_cli_kind_receives_derived_files`
      — acceptance: exits 0 and proves that the local leaf receives only `a.md` and `b.md` and its
      fixture exit code is propagated.

- [ ] [AI] **P1-DISPATCH-KIND-RHINO-REFACTOR** (`blockedBy: P1-DISPATCH-KIND-RHINO-GREEN`;
      `blocks: P1-DISPATCH-KIND-EXTERNAL-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, extract the `rhino-cli` argv assembly without adding another
      kind. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch rhino_cli_kind_receives_derived_files`
      — acceptance: exits 0 with the same derived-file order and exit propagation.

- [ ] [AI] **P1-DISPATCH-KIND-EXTERNAL-RED** (`blockedBy: P1-DISPATCH-KIND-RHINO-REFACTOR`;
      `blocks: P1-DISPATCH-KIND-EXTERNAL-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `external_kind_preserves_fixed_argv_before_files` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch external_kind_preserves_fixed_argv_before_files`
      — acceptance: fails because PATH-resolved external dispatch does not yet preserve fixed argv
      before derived files.

  **Gherkin (binds) →** "External kind preserves fixed argv before files"

  ```gherkin
  Scenario: External kind preserves fixed argv before files
    Given an external gate declares "shellcheck --severity=warning" and matches "tool.sh"
    When "rhino-cli gate run --surface=ci --only=shellcheck" runs
    Then PATH-resolved shellcheck receives "--severity=warning" then "tool.sh"
  ```

- [ ] [AI] **P1-DISPATCH-KIND-EXTERNAL-GREEN** (`blockedBy: P1-DISPATCH-KIND-EXTERNAL-RED`;
      `blocks: P1-DISPATCH-KIND-EXTERNAL-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only PATH-resolved external dispatch with declared
      argv preceding derived files. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch external_kind_preserves_fixed_argv_before_files`
      — acceptance: exits 0 and records `--severity=warning` before `tool.sh`.

- [ ] [AI] **P1-DISPATCH-KIND-EXTERNAL-REFACTOR** (`blockedBy: P1-DISPATCH-KIND-EXTERNAL-GREEN`;
      `blocks: P1-DISPATCH-KIND-NX-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, reuse argv assembly for the external branch without adding
      Nx behavior. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch external_kind_preserves_fixed_argv_before_files`
      — acceptance: exits 0 with the same PATH resolution and exact argv order.

- [ ] [AI] **P1-DISPATCH-KIND-NX-RED** (`blockedBy: P1-DISPATCH-KIND-EXTERNAL-REFACTOR`;
      `blocks: P1-DISPATCH-KIND-NX-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `nx_kind_delegates_affected_project_graph` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch nx_kind_delegates_affected_project_graph`
      — acceptance: fails because Nx kind dispatch does not yet delegate through
      `npm exec nx -- affected -t test:quick` or propagate its exit code.

  **Gherkin (binds) →** "Nx kind delegates the affected project graph"

  ```gherkin
  Scenario: Nx kind delegates the affected project graph
    Given an nx gate "test:quick" declares scope "affected-projects"
    When "rhino-cli gate run --surface=pre-push --only=test-quick" runs
    Then "npm exec nx -- affected -t test:quick" runs and its exit code is propagated
  ```

- [ ] [AI] **P1-DISPATCH-KIND-NX-GREEN** (`blockedBy: P1-DISPATCH-KIND-NX-RED`;
      `blocks: P1-DISPATCH-KIND-NX-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only Nx affected-target delegation and exit
      propagation. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch nx_kind_delegates_affected_project_graph`
      — acceptance: exits 0 and records exactly `npm exec nx -- affected -t test:quick` with the
      fixture exit code propagated.

- [ ] [AI] **P1-DISPATCH-KIND-NX-REFACTOR** (`blockedBy: P1-DISPATCH-KIND-NX-GREEN`;
      `blocks: P1-DISPATCH-SCOPES-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, centralize completed kind selection without changing any
      kind contract. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch nx_kind_delegates_affected_project_graph`
      — acceptance: exits 0 with the exact Nx argv and exit propagation unchanged.

- [ ] [AI] **P1-DISPATCH-SCOPES-RED** (`blockedBy: P1-DISPATCH-KIND-NX-REFACTOR`;
      `blocks: P1-DISPATCH-SCOPES-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `all_supported_scopes_derive_specified_inputs` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch all_supported_scopes_derive_specified_inputs`
      — acceptance: fails because at least one of the six scope input contracts is absent.

  **Gherkin (binds) →** "All supported scopes derive their specified inputs"

  ```gherkin
  Scenario: All supported scopes derive their specified inputs
    Given one fixture registry covers affected-file-type, all-file-type, affected-projects, all-projects, other, and path-gated
    When each gate runs through "gate run --only" on its valid surface
    Then each leaf receives exactly its staged, tracked, affected, complete, empty, or trigger-intersection input contract
  ```

- [ ] [AI] **P1-DISPATCH-SCOPES-GREEN** (`blockedBy: P1-DISPATCH-SCOPES-RED`;
      `blocks: P1-DISPATCH-SCOPES-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only the six declared scope derivations. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch all_supported_scopes_derive_specified_inputs`
      — acceptance: exits 0 and every leaf receives exactly its staged, tracked, affected,
      complete, empty, or trigger-intersection repository-relative input set.

- [ ] [AI] **P1-DISPATCH-SCOPES-REFACTOR** (`blockedBy: P1-DISPATCH-SCOPES-GREEN`;
      `blocks: P1-DISPATCH-FILTER-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, extract pure scope candidate derivation without applying
      glob/exclude filtering. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch all_supported_scopes_derive_specified_inputs`
      — acceptance: exits 0 with all six exact input contracts unchanged.

- [ ] [AI] **P1-DISPATCH-FILTER-RED** (`blockedBy: P1-DISPATCH-SCOPES-REFACTOR`;
      `blocks: P1-DISPATCH-FILTER-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `glob_lists_and_excludes_apply_before_invocation` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch glob_lists_and_excludes_apply_before_invocation`
      — acceptance: fails because candidate glob-list and exclusion filtering is absent or occurs
      after leaf invocation.

  **Gherkin (binds) →** "Glob lists and excludes are applied before invocation"

  ```gherkin
  Scenario: Glob lists and excludes are applied before invocation
    Given a file gate has globs "*.md" and "*.yml" and excludes "plans/done"
    When its candidate set contains matching, non-matching, and excluded paths
    Then the leaf receives only matching non-excluded repository-relative paths
  ```

- [ ] [AI] **P1-DISPATCH-FILTER-GREEN** (`blockedBy: P1-DISPATCH-FILTER-RED`;
      `blocks: P1-DISPATCH-FILTER-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only glob/globs and exclude filtering before
      invocation. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch glob_lists_and_excludes_apply_before_invocation`
      — acceptance: exits 0 and the leaf receives only matching, non-excluded,
      repository-relative fixture paths.

- [ ] [AI] **P1-DISPATCH-FILTER-REFACTOR** (`blockedBy: P1-DISPATCH-FILTER-GREEN`;
      `blocks: P1-DISPATCH-EMPTY-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, extract pure candidate filtering without adding empty-set
      skip behavior. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch glob_lists_and_excludes_apply_before_invocation`
      — acceptance: exits 0 with the same exact filtered path set and pre-invocation ordering.

- [ ] [AI] **P1-DISPATCH-EMPTY-RED** (`blockedBy: P1-DISPATCH-FILTER-REFACTOR`;
      `blocks: P1-DISPATCH-EMPTY-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `empty_scoped_match_is_successful_skip` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch empty_scoped_match_is_successful_skip`
      — acceptance: fails because a filtered empty file set still invokes the leaf or exits
      non-zero.

  **Gherkin (binds) →** "An empty scoped match is a successful skip"

  ```gherkin
  Scenario: An empty scoped match is a successful skip
    Given a file-scoped gate has no path after glob and exclusion filtering
    When that gate runs
    Then it exits zero without invoking the leaf and reports the skip
  ```

- [ ] [AI] **P1-DISPATCH-EMPTY-GREEN** (`blockedBy: P1-DISPATCH-EMPTY-RED`;
      `blocks: P1-DISPATCH-EMPTY-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only successful empty-set skipping and reporting.
      Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch empty_scoped_match_is_successful_skip`
      — acceptance: exits 0, invokes no leaf, and records the fixture skip.

- [ ] [AI] **P1-DISPATCH-EMPTY-REFACTOR** (`blockedBy: P1-DISPATCH-EMPTY-GREEN`;
      `blocks: P1-DISPATCH-ONLY-VALID-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, isolate empty-set reporting without changing invocation
      behavior. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch empty_scoped_match_is_successful_skip`
      — acceptance: exits 0 with no leaf invocation and the same skip record.

- [ ] [AI] **P1-DISPATCH-ONLY-VALID-RED** (`blockedBy: P1-DISPATCH-EMPTY-REFACTOR`;
      `blocks: P1-DISPATCH-ONLY-VALID-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `only_executes_exactly_one_direct_leaf` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch only_executes_exactly_one_direct_leaf`
      — acceptance: fails because a valid `--only` request executes an unrelated batch or
      mutation, or passes inputs outside the selected leaf's match.

  **Gherkin (binds) →** "Only executes exactly one direct leaf"

  ```gherkin
  Scenario: Only executes exactly one direct leaf
    Given pre-commit declares two batch entries and one direct mutation
    When "gate run --surface=pre-commit --only=md-mermaid" runs
    Then only md-mermaid runs directly with its matching files and no batch or mutation runs
  ```

- [ ] [AI] **P1-DISPATCH-ONLY-VALID-GREEN** (`blockedBy: P1-DISPATCH-ONLY-VALID-RED`;
      `blocks: P1-DISPATCH-ONLY-VALID-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only valid direct exactly-one selection. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch only_executes_exactly_one_direct_leaf`
      — acceptance: exits 0 and runs only `md-mermaid` directly with its matching files, spawning
      no batch or mutation.

- [ ] [AI] **P1-DISPATCH-ONLY-VALID-REFACTOR** (`blockedBy: P1-DISPATCH-ONLY-VALID-GREEN`;
      `blocks: P1-DISPATCH-ONLY-INVALID-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, extract selected-leaf dispatch without adding invalid-id
      handling. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch only_executes_exactly_one_direct_leaf`
      — acceptance: exits 0 with one direct leaf, its bounded inputs, and no aggregate lint-staged
      process.

- [ ] [AI] **P1-DISPATCH-ONLY-INVALID-RED** (`blockedBy: P1-DISPATCH-ONLY-VALID-REFACTOR`;
      `blocks: P1-DISPATCH-ONLY-INVALID-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `unknown_or_duplicate_only_ids_fail_before_execution` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch unknown_or_duplicate_only_ids_fail_before_execution`
      — acceptance: fails because an absent or duplicate `--only` id reaches leaf execution or
      does not name the invalid id.

  **Gherkin (binds) →** "Unknown or duplicate only ids fail before execution"

  ```gherkin
  Scenario: Unknown or duplicate only ids fail before execution
    Given the requested only id is absent or duplicated in the fixture registry
    When "gate run --surface=ci --only=unknown" runs
    Then it exits non-zero before invoking any leaf and names the invalid id
  ```

- [ ] [AI] **P1-DISPATCH-ONLY-INVALID-GREEN** (`blockedBy: P1-DISPATCH-ONLY-INVALID-RED`;
      `blocks: P1-DISPATCH-ONLY-INVALID-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only pre-execution absent/duplicate id rejection.
      Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch unknown_or_duplicate_only_ids_fail_before_execution`
      — acceptance: exits 0 as a test and proves both invalid fixtures return non-zero, invoke no
      leaf, and name the invalid id.

- [ ] [AI] **P1-DISPATCH-ONLY-INVALID-REFACTOR** (`blockedBy: P1-DISPATCH-ONLY-INVALID-GREEN`;
      `blocks: P1-DISPATCH-RESTAGE-SUCCESS-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, share id validation between list/run without changing the
      failure boundary. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch unknown_or_duplicate_only_ids_fail_before_execution`
      — acceptance: exits 0 and both invalid fixtures still fail before any leaf invocation with
      the invalid id named.

- [ ] [AI] **P1-DISPATCH-RESTAGE-SUCCESS-RED** (`blockedBy: P1-DISPATCH-ONLY-INVALID-REFACTOR`;
      `blocks: P1-DISPATCH-RESTAGE-SUCCESS-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `restaging_mutation_stages_only_outputs` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch restaging_mutation_stages_only_outputs`
      — acceptance: fails because successful mutation output isolation/restaging is absent or
      stages the unrelated worktree edit.

  **Gherkin (binds) →** "A re-staging mutation stages only its outputs"

  ```gherkin
  Scenario: A re-staging mutation stages only its outputs
    Given an unrelated worktree edit exists and a successful restaging mutation changes generated paths
    When the mutation runs through pre-commit
    Then git adds only the mutation output paths and preserves the unrelated edit unstaged
  ```

- [ ] [AI] **P1-DISPATCH-RESTAGE-SUCCESS-GREEN** (`blockedBy: P1-DISPATCH-RESTAGE-SUCCESS-RED`;
      `blocks: P1-DISPATCH-RESTAGE-SUCCESS-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only exact-output restaging after a zero exit.
      Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch restaging_mutation_stages_only_outputs`
      — acceptance: exits 0, `git add --` receives only mutation output paths, and the unrelated
      edit remains unstaged.

- [ ] [AI] **P1-DISPATCH-RESTAGE-SUCCESS-REFACTOR** (`blockedBy: P1-DISPATCH-RESTAGE-SUCCESS-GREEN`;
      `blocks: P1-DISPATCH-RESTAGE-FAILURE-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, extract the successful index snapshot/delta calculation
      without adding failure handling. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch restaging_mutation_stages_only_outputs`
      — acceptance: exits 0 and `git add --` still receives only explicit mutation output paths.

- [ ] [AI] **P1-DISPATCH-RESTAGE-FAILURE-RED** (`blockedBy: P1-DISPATCH-RESTAGE-SUCCESS-REFACTOR`;
      `blocks: P1-DISPATCH-RESTAGE-FAILURE-GREEN`) — RED: in
      `apps/rhino-cli/tests/gate_dispatch.rs`, add failing
      `failed_mutation_never_restages_output` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch failed_mutation_never_restages_output`
      — acceptance: fails because a non-zero mutation still reaches restaging or its failure is
      not propagated.

  **Gherkin (binds) →** "A failed mutation never re-stages output"

  ```gherkin
  Scenario: A failed mutation never re-stages output
    Given a restaging mutation returns non-zero after changing a path
    When the mutation runs through pre-commit
    Then the dispatcher exits non-zero and does not git-add that path
  ```

- [ ] [AI] **P1-DISPATCH-RESTAGE-FAILURE-GREEN** (`blockedBy: P1-DISPATCH-RESTAGE-FAILURE-RED`;
      `blocks: P1-DISPATCH-RESTAGE-FAILURE-REFACTOR`) — GREEN: in
      `apps/rhino-cli/src/commands.rs`, implement only the non-zero mutation short-circuit before
      restaging. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch failed_mutation_never_restages_output`
      — acceptance: exits 0 as a test and proves the dispatcher returns the fixture failure while
      `git add --` receives no path.

- [ ] [AI] **P1-DISPATCH-RESTAGE-FAILURE-REFACTOR** (`blockedBy: P1-DISPATCH-RESTAGE-FAILURE-GREEN`;
      `blocks: P1-DISPATCH-BATCH-RED`) — REFACTOR: in
      `apps/rhino-cli/src/commands.rs`, make the success-only restaging boundary explicit without
      changing failure behavior. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch failed_mutation_never_restages_output`
      — acceptance: exits 0 and the failing mutation still returns non-zero without any `git add`
      invocation.

- [ ] [AI] **P1-DISPATCH-BATCH-RED** (`blockedBy: P1-DISPATCH-RESTAGE-FAILURE-REFACTOR`; `blocks: P1-DISPATCH-BATCH-GREEN`) — RED: add failing
      `precommit_has_one_ordered_file_batch` (**new test**). Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch precommit_has_one_ordered_file_batch`
      — acceptance: fails because the aggregate batch position/consumption rule is absent.

  **Gherkin (binds) →** "Pre-commit has one declaration-positioned batch"

  ```gherkin
  Scenario: Pre-commit has one declaration-positioned batch
    Given staged guard precedes file entries and two direct mutations follow them in declaration order
    When "gate run --surface=pre-commit" runs
    Then staged guard, exactly one lint-staged batch, harness generation, and lockfile sync run in that order
  ```

- [ ] [AI] **P1-DISPATCH-BATCH-GREEN** (`blockedBy: P1-DISPATCH-BATCH-RED`; `blocks: P1-DISPATCH-BATCH-REFACTOR`) — GREEN:
      implement one batch at the first eligible declaration and direct trailing mutations. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch precommit_has_one_ordered_file_batch`
      — acceptance: exits 0 and records staged guard → one lint-staged process → harness generation
      → lockfile sync, with no direct duplicate file leaf.
- [ ] [AI] **P1-DISPATCH-BATCH-REFACTOR** (`blockedBy: P1-DISPATCH-BATCH-GREEN`; `blocks: P1-VALIDATE`) — REFACTOR:
      name and document the batch eligibility predicate. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_dispatch precommit_has_one_ordered_file_batch`
      — acceptance: exits 0 and lockfile sync is absent from emitted lint-staged JSON.

### 1.4 `gate validate`

- [ ] [AI] **RED** — failing test for check 1 in
      [tech-docs §2.4](./tech-docs.md#24-command-surface): a `type: check` gate declared for
      `pre-commit` but not for `ci`, with no carve-out, violates the composition rule — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::composition_rule_violation`
      — acceptance: fails because the command does not exist.

  **Gherkin (binds) →** "A check declared for pre-commit but not for ci violates the composition rule"

  ```gherkin
  Scenario: A check declared for pre-commit but not for ci violates the composition rule
    Given a gate declares type "check" and surface "pre-commit"
    And that gate declares no surface "ci"
    And that gate carries no carve-out
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message cites the Gate Composition Rule
    And the message names the gate id and the missing surface
  ```

- [ ] [AI] **GREEN** — implement `gate validate` with the composition-rule check — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::composition_rule_violation`
      — acceptance: the new test passes.
- [ ] [AI] **REFACTOR** — the composition-rule check applies to `type: check` only, and
      `carve-out: staged-only` exempts a check from it — acceptance: four tests, all required
      because each covers a direction the others do not: a `type: mutation` gate with `pre-commit`
      only **passes**; a `carve-out: staged-only` check with `pre-commit` only **passes**; an
      unmarked `type: check` with `pre-commit` only **fails**; and `gate list` reports the
      exemption. A one-direction test set would pass on a validator that never fires.
- [ ] [AI] **RED** — failing test for check 2: a surface file that stops invoking the registry is
      caught — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::missing_surface_shim`
      — acceptance: fails because check 2 does not exist yet.

  **Gherkin (binds) →** "A surface file that stops invoking the registry is caught"

  ```gherkin
  Scenario: A surface file that stops invoking the registry is caught
    Given the registry declares gates on surface "pre-push"
    And ".husky/pre-push" does not invoke "gate run --surface=pre-push"
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the surface file
  ```

- [ ] [AI] **GREEN** — implement check 2 (missing surface shim) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::missing_surface_shim` — acceptance:
      the new test passes, no other tests broken.
- [ ] [AI] **RED** — failing test for check 3's undeclared-command half: a CI workflow that
      hardcodes a check instead of deriving it is caught — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::undeclared_ci_command`
      — acceptance: fails because check 3 does not exist yet.

  **Gherkin (binds) →** "A CI workflow that hardcodes a check instead of deriving it is caught"

  ```gherkin
  Scenario: A CI workflow that hardcodes a check instead of deriving it is caught
    Given "pr-quality-gate.yml" runs a check command that no registry gate declares
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the undeclared command
  ```

- [ ] [AI] **GREEN** — implement the undeclared-CI-command half of check 3 — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::undeclared_ci_command` —
      acceptance: the new test passes, no other tests broken.
- [ ] [AI] **RED** — failing test for check 4: a `verifies` field naming no existing gate is caught
      — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::orphan_verifies_reference`
      — acceptance: fails because check 4 does not exist yet.

  **Gherkin (binds) →** "A verifies field naming no existing gate is caught"

  ```gherkin
  Scenario: A verifies field naming no existing gate is caught
    Given a gate carries "verifies" naming an id no gate declares
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names both the referring gate id and the orphan id
  ```

- [ ] [AI] **GREEN** — implement check 4 (orphan `verifies` reference) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::orphan_verifies_reference` —
      acceptance: the new test passes, no other tests broken.
- [ ] [AI] **RED** — failing test for check 5: a hand-edited `lint-staged` block (diverging from
      what the registry would emit) is caught — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::stale_lint_staged_block`
      — acceptance: fails because check 5 does not exist yet.

  **Gherkin (binds) →** "A hand-edited lint-staged block is caught"

  ```gherkin
  Scenario: A hand-edited lint-staged block is caught
    Given the "lint-staged" block in package.json differs from what the registry would emit
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names package.json and instructs to run "gate emit --surface=pre-commit"
  ```

- [ ] [AI] **GREEN** — implement check 5 (stale emitted `lint-staged` block) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::stale_lint_staged_block`
      — acceptance: the new test passes, no other tests broken.
- [ ] [AI] **RED** — failing test for check 6: a formatter mutation gate with no `verifies`-linked
      check is caught — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::unverified_formatter`
      — acceptance: fails because check 6 does not exist yet.

  **Gherkin (binds) →** "A formatter without a verifying check fails validation"

  ```gherkin
  Scenario: A formatter without a verifying check fails validation
    Given a gate declares type "mutation" and a formatter command
    And no gate declares a "verifies" field naming that gate id
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the unverified formatter
  ```

- [ ] [AI] **GREEN** — implement check 6 (unverified formatter) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::unverified_formatter` — acceptance:
      the new test passes, no other tests broken, and `nx run rhino-cli:test:quick` still exits 0 for
      the six checks introduced across this section.
- [ ] [AI] **RED** — add a failing test in the `gate::validate` module for check 3's `wiring` split:
      a `hand-wired` gate with a matching workflow job must pass validation — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::hand_wired_present`
      — acceptance: fails because the `wiring: hand-wired` check-3 split does not exist yet.

  **Gherkin (binds) →** "A hand-wired gate is asserted present but not matrix-derived"

  ```gherkin
  Scenario: A hand-wired gate is asserted present but not matrix-derived
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    And "pr-quality-gate.yml" contains a job invoking "test:quick"
    When "rhino-cli gate validate" runs
    Then it exits zero
  ```

- [ ] [AI] **GREEN** — implement the `hand-wired`-present-and-matched half of check 3's `wiring`
      split — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::hand_wired_present`
      — acceptance: the new test passes, no other tests broken.
- [ ] [AI] **RED** — add a failing test in the `gate::validate` module for check 3's `wiring` split:
      the same `hand-wired` gate with its workflow job deleted must fail validation — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::hand_wired_job_deleted`
      — acceptance: fails because the job-deleted half of the split does not exist yet.

  **Gherkin (binds) →** "A hand-wired gate whose job was deleted is caught"

  ```gherkin
  Scenario: A hand-wired gate whose job was deleted is caught
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    And "pr-quality-gate.yml" contains no job invoking "test:quick"
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the gate id and the surface file
  ```

- [ ] [AI] **GREEN** — implement the job-deleted half of check 3's `wiring` split — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate::hand_wired_job_deleted`
      — acceptance: the new test passes and each command that runs the check-3 tests exits 0, no
      other tests broken.

### 1.5 Specs and coverage

- [ ] [AI] Author the Gherkin feature files under
      `specs/apps/rhino/behavior/rhino-cli/gherkin/` from the scenarios in
      [prd.md](./prd.md), with `@covers` markers — acceptance:
      `npx nx run rhino-cli:specs:behavior:coverage` exits 0.
- [ ] [AI] **P1-SPECS** — Verify structural specs and coverage floor — acceptance:
      `npx nx run rhino-cli:test:quick` exits 0 (this chains typecheck, lint, unit, coverage, specs).

### Phase 1 Execution-Ready Gate

- [ ] [AI] **P1-READY** (`blockedBy: P1-SPECS`; `blocks: P1-LAND`) — command:
      `git status --short && npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` —
      acceptance: the reconciled task ledger is clean and every command exits 0 before any Land
      action begins.

### 1.6 Land

Every non-merge checkbox in this subsection is `blockedBy: P1-READY`; the untagged protected merge
checkbox remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit the Phase 1 theme — command:
      `git add -- apps/rhino-cli specs/apps/rhino/behavior/rhino-cli/gherkin docs/reference/sdlc-gate-standard.md docs/reference/related-repositories.md && git diff --cached --name-only -- apps/rhino-cli specs/apps/rhino/behavior/rhino-cli/gherkin | grep -q . && git commit -m 'feat(rhino-cli): add registry-driven gate engine'` — acceptance:
      commitlint and `npm run validate:sync` exit 0; the staged diff contains both the engine and
      its required Gherkin, and generated mirrors, if changed, are included in this commit.
- [ ] [AI] Push Phase 1 — command: `git push -u origin sdlc-gate-registry-enforcement` — acceptance: exits 0.
- [ ] [AI] Open its draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement --fill` — acceptance: `gh pr view --json number,url` returns one PR.
- [ ] [AI] Cycle 1 maker fan-out — invoke all eight `pr-review-*-maker` disciplines with the URL from `gh pr view --json url --jq .url` — acceptance: eight reports exist.
- [ ] [AI] Cycle 1 synthesis — invoke `pr-review-synthesis-maker` on those reports — acceptance: one review of record is posted.
- [ ] [AI] Cycle 1 fixer — invoke `pr-review-fixer` on that review — acceptance: every accepted finding is fixed, committed, and pushed.
- [ ] [AI] Cycle 1 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; otherwise fix all failures, commit, push, and repeat before Cycle 2.
- [ ] [AI] Cycle 2 maker fan-out — invoke all eight `pr-review-*-maker` disciplines on the updated PR — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 2 synthesis — invoke `pr-review-synthesis-maker` — acceptance: one fresh review of record is posted.
- [ ] [AI] Cycle 2 fixer — invoke `pr-review-fixer` — acceptance: every accepted finding is fixed, committed, and pushed.
- [ ] [AI] Cycle 2 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; failures are fixed and pushed before Cycle 3.
- [ ] [AI] Cycle 3 maker fan-out — invoke all eight `pr-review-*-maker` disciplines on the updated PR — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 3 synthesis — invoke `pr-review-synthesis-maker` — acceptance: one fresh review of record is posted.
- [ ] [AI] Cycle 3 fixer — invoke `pr-review-fixer` — acceptance: every accepted finding is fixed, committed, and pushed.
- [ ] [AI] Cycle 3 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; failures are fixed and pushed before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: `gh pr view --json isDraft --jq .isDraft` prints `false` and all five hardened merge preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 1 Gate

> These checks verify the authorized integration after Land completes.
> **Byte-identity transaction opened at integration** —
> `apps/rhino-cli` in `ose-public` now differs from every other repo. Do **not** start Phases 2, 3,
> 4 or 5 from this gate, only from the Phase 11 gate — copying canonical now would propagate the
> hardcoded app names Phase 11 exists to remove.

- [ ] [AI] `gate list`, `gate run`, `gate emit`, `gate validate`, and `git lockfile sync` all exist
      and are tested — acceptance: `npx nx run rhino-cli:test:quick` exits 0.
- [ ] [AI] No surface is wired to the new commands yet — acceptance:
      `grep -rn "gate run\|gate validate" .husky/ .github/workflows/` returns no match (Phase 2
      wires them).
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.

> **Pause Safety**: the integrated gate engine is inert, the phase checks are green, and the four
> refs plus Phase 11 as the next node are recorded in the bounded transaction ledger. This controlled
> checkpoint is safe to stop, but not safe for unrelated boundary work or an identity-restored claim.
> To resume: run the four exact `rev-parse origin/main` commands in the transaction protocol, compare
> them with the ledger, and continue Phase 11.

---

## Phase 11 — De-fork Canonical Source and Add the Parity Manifest (`ose-public`, PR #1b)

Delivery unit: `apps/rhino-cli`'s canonical source contains no repository's app names, the dead
pre-commit pipeline is gone, `beaver-nest`'s general improvements are upstreamed, and a checksum
manifest plus its gate exist. After this checkpoint, canonical is copyable to any repo without
carrying `ose-public`-specific data into it. It is reversible but remains inside the open propagation
transaction; it does not claim four-repo identity is restored before propagation.

**This phase directly blocks Phase 2 and transitively blocks Phases 3, 4, and 5.** Copying a canonical
that still hardcodes `ose-public`'s app names would either recreate `beaver-nest`'s fork or delete
capabilities it depends on. See
[tech-docs §2.8.5](./tech-docs.md#285-convergence-sequence--upstream-before-downstream).

- [ ] [AI] Create the Phase 11 worktree from the merged Phase 1 state — commands:
      `git fetch origin main` and
      `git worktree add -b sdlc-gate-registry-enforcement-defork worktrees/sdlc-gate-registry-enforcement-defork origin/main`
      — acceptance: the worktree is clean and `HEAD...origin/main` reports `0 0`.
- [ ] [AI] Install dependencies in the Phase 11 worktree — command:
      `npm --prefix worktrees/sdlc-gate-registry-enforcement-defork install` — acceptance: exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd worktrees/sdlc-gate-registry-enforcement-defork && npm run doctor -- --fix)` — acceptance:
      exits 0 and the follow-up doctor check reports no missing tool.
- [ ] [AI] **P11-PRESERVE-CANONICAL-FIXES** — before composing Beaver's improvements, retain
      public's scope-correct non-discovery Git-state handling, `CwdLock` repo-config reads, and
      serialized Git-sensitive unit-test layout; add inherited-Git-variable clearing to each
      serialized test command without collapsing them into a parallel command — acceptance:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test cargo_target_share` and
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven` exit 0;
      `project.json` retains sequential `test:unit` commands, each prefixed with all three `env -u`
      variables, and focused Git-state regressions remain green.

### 11.1 Delete the dead pre-commit pipeline

Blast radius is seven sites — [tech-docs §2.8.2](./tech-docs.md#282-the-dead-pre-commit-pipeline).

- [ ] [AI] **RED** — prove the pipeline is unreachable before deleting it: assert that no CLI
      subcommand dispatches to `commands/git_pre_commit.rs` — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- --help > /tmp/help-before.txt`
      succeeds, and `/usr/bin/grep -rn "git_pre_commit" apps/rhino-cli/src/cli.rs` returns no match.
      Record `help-before.txt`; it is the acceptance oracle for the deletion.

  **Gherkin (binds) →** "The dead pre-commit pipeline is removed"

  ```gherkin
  Scenario: The dead pre-commit pipeline is removed
    Given commands/git_pre_commit.rs is wired to no CLI subcommand
    When it and application/git/pre_commit.rs are deleted
    Then "cargo build --release" succeeds
    And the full test suite passes
    And "rhino-cli --help" lists the same commands as before the deletion
  ```

- [ ] [AI] **P1B-DEAD-1** (`blocks: P1B-DEAD-2`) — delete
      `apps/rhino-cli/src/application/git/pre_commit.rs` — command:
      `git rm apps/rhino-cli/src/application/git/pre_commit.rs` — acceptance: path is staged deleted.
- [ ] [AI] **P1B-DEAD-2** (`blockedBy: P1B-DEAD-1`; `blocks: P1B-DEAD-3`) — delete
      `apps/rhino-cli/src/commands/git_pre_commit.rs` — command:
      `git rm apps/rhino-cli/src/commands/git_pre_commit.rs` — acceptance: path is staged deleted.
- [ ] [AI] **P1B-DEAD-3** (`blockedBy: P1B-DEAD-2`; `blocks: P1B-DEAD-4`) — remove the module declaration from
      `apps/rhino-cli/src/commands.rs` — command:
      `rg -n "git_pre_commit" apps/rhino-cli/src/commands.rs` — acceptance: exits 1 after the edit.
- [ ] [AI] **P1B-DEAD-4** (`blockedBy: P1B-DEAD-3`; `blocks: P1B-DEAD-5`) — remove the re-export from
      `apps/rhino-cli/src/internal/git.rs` — command:
      `rg -n "pre_commit" apps/rhino-cli/src/internal/git.rs` — acceptance: exits 1 after the edit.
- [ ] [AI] **P1B-DEAD-5** (`blockedBy: P1B-DEAD-4`; `blocks: P1B-DEAD-6`) — remove only the orphaned `Deps` implementation from
      `apps/rhino-cli/src/infrastructure/git/mod.rs` — command:
      `cargo check --manifest-path apps/rhino-cli/Cargo.toml` — acceptance: exits 0.
- [ ] [AI] **P1B-DEAD-6** (`blockedBy: P1B-DEAD-5`; `blocks: P1B-DEAD-7`) — delete orphaned
      `apps/rhino-cli/src/domain/git/staged_files.rs` — command:
      `git rm apps/rhino-cli/src/domain/git/staged_files.rs` — acceptance: path is staged deleted.
- [ ] [AI] **P1B-DEAD-7** (`blockedBy: P1B-DEAD-6`; `blocks: P1B-DEAD-VALIDATE`) — update the stale reference in
      `apps/rhino-cli/src/application/fs/mock.rs` — command:
      `rg -n "pre_commit|staged_files" apps/rhino-cli/src/application/fs/mock.rs` — acceptance: exits 1.
- [ ] [AI] **P1B-DEAD-VALIDATE** (`blockedBy: P1B-DEAD-7`) — command:
      `cargo build --release --manifest-path apps/rhino-cli/Cargo.toml && npm exec nx -- run rhino-cli:test:quick && diff /tmp/help-before.txt <(cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- --help)`
      — acceptance: exits 0; changed help means the code was not dead.
- [ ] [AI] **REFACTOR** — confirm the largest hardcoded-paths site is gone — acceptance:
      `/usr/bin/grep -rn "ayokoding" apps/rhino-cli/src/` returns no match. Verify the inverse holds
      pre-edit: the same command returns matches before the deletion.

### 11.2 Extract repo-specific data into `repo-config.yml`

- [ ] [AI] **P1B-WEBSITE-RED** (`blocks: P1B-WEBSITE-GREEN`) — RED: add
      `website_prefix_exclusions_are_runtime_config` (**new test**) to
      `apps/rhino-cli/tests/repo_config_data_driven.rs`, bound to the R-13 extraction scenario. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven website_prefix_exclusions_are_runtime_config`
      — acceptance: fails because frontmatter audit still reads `WEBSITE_APP_PREFIXES`.

  **Gherkin (binds) →** "Gate exclusion lists move to the registry"

  ```gherkin
  Scenario: Gate exclusion lists move to the registry
    Given WEBSITE_APP_PREFIXES was a hardcoded const in frontmatter_audit.rs
    When convergence completes
    Then those paths are declared as "args.exclude" on the gate that consumes them
    And the const no longer exists in source
  ```

- [ ] [AI] **P1B-WEBSITE-GREEN** (`blockedBy: P1B-WEBSITE-RED`; `blocks: P1B-WEBSITE-REFACTOR`) — GREEN:
      make frontmatter audit consume `args.exclude` and delete the constant. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven website_prefix_exclusions_are_runtime_config`
      — acceptance: exits 0 and a configured failing fixture under an excluded tree is skipped.
- [ ] [AI] **P1B-WEBSITE-REFACTOR** (`blockedBy: P1B-WEBSITE-GREEN`; `blocks: P1B-AMAZON-RED`) — REFACTOR:
      remove the last constant references. Run
      `/usr/bin/grep -rho "WEBSITE_APP_PREFIXES" apps/rhino-cli/src/ | /usr/bin/wc -l` — acceptance:
      prints `0`; then
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven website_prefix_exclusions_are_runtime_config`
      exits 0.
- [ ] [AI] **P1B-AMAZON-RED** (`blockedBy: P1B-WEBSITE-REFACTOR`; `blocks: P1B-AMAZON-GREEN`) — RED: add
      `amazon_q_definition_name_comes_from_harness_config` (**new test**) to
      `apps/rhino-cli/tests/repo_config_data_driven.rs`, bound to the R-13 extraction scenario. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven amazon_q_definition_name_comes_from_harness_config`
      — acceptance: fails because `bindings.rs` still hardcodes the name.

  **Gherkin (binds) →** "Amazon Q definition name moves to harness configuration"

  ```gherkin
  Scenario: Amazon Q definition name moves to harness configuration
    Given bindings.rs hardcoded the Amazon Q definition name
    When convergence completes
    Then harness.amazonq.agent-name supplies the generated filename and embedded definition name
    And the definition name no longer exists in shared Rust source
  ```

- [ ] [AI] **P1B-AMAZON-GREEN** (`blockedBy: P1B-AMAZON-RED`; `blocks: P1B-AMAZON-REFACTOR`) — GREEN:
      read the definition name from `harness.amazonq.agent-name`. Run
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven amazon_q_definition_name_comes_from_harness_config`
      — acceptance: exits 0 and generation writes `.amazonq/cli-agents/ose-default.json` because
      `repo-config.yml`, not Rust source, declares `ose-default`.
- [ ] [AI] **P1B-AMAZON-REFACTOR** (`blockedBy: P1B-AMAZON-GREEN`; `blocks: P1B-FIXTURE-NAMES`) — REFACTOR:
      remove embedded definition-name literals. Run
      `/usr/bin/grep -rho "ose-default" apps/rhino-cli/src/ | /usr/bin/wc -l` — acceptance: prints
      `0`; then
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven amazon_q_definition_name_comes_from_harness_config`
      exits 0.
- [ ] [AI] **P1B-FIXTURE-NAMES** (`blockedBy: P1B-AMAZON-REFACTOR`; `blocks: P1B-DOC-COMMENT`) — replace real-repo app names in test fixtures with synthetic names in
      `domain_coverage/mod.rs`, `specs_validate_counts.rs`, and `specs_coverage.rs` — acceptance:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
      exits 0. Fixtures name no real repository's apps.
- [ ] [AI] **P1B-DOC-COMMENT** (`blockedBy: P1B-FIXTURE-NAMES`) — genericize the
      `apps/ose-be/global.json` doc comment in `doctor/tools.rs`. Run
      `rg -n "ayokoding|organiclever|ose-be|ose-www|wahidyankf" apps/rhino-cli/src/application/domain_coverage/mod.rs apps/rhino-cli/src/commands/specs_validate_counts.rs apps/rhino-cli/src/commands/specs_coverage.rs apps/rhino-cli/src/application/doctor/tools.rs`
      — acceptance: exits 1 with no matches. The gate is intentionally bounded to the enumerated
      shared-data sites; unrelated environment-contract examples are outside this extraction.

### 11.3 Upstream `beaver-nest`'s improvements

Direction matters: these flow **up** into canonical before any repo copies canonical **down**.

- [ ] [AI] **RED** — add a failing test asserting `ROADMAP.md` and `SECURITY.md` are exempt from
      `md naming validate` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib docs::naming` — acceptance: fails
      on canonical, which currently exempts neither.

  **Gherkin (binds) →** "beaver-nest's naming exemptions are upstreamed before any copy"

  ```gherkin
  Scenario: beaver-nest's naming exemptions are upstreamed before any copy
    Given beaver-nest exempts ROADMAP.md and SECURITY.md from md naming validate
    And canonical ose-public does not
    When Phase 11 completes
    Then canonical exempts both
    And "md naming validate" passes on a ROADMAP.md fixture in ose-public
    And this holds before any downstream repo copies canonical
  ```

- [ ] [AI] **GREEN** — add both basenames to `is_naming_exempt`'s always-exempt list in `naming.rs`,
      matching `beaver-nest`'s implementation — acceptance: the same test passes, and
      `md naming validate` exits 0 on a `ROADMAP.md` fixture.
- [ ] [AI] Port `beaver-nest`'s corrected `frontmatter_audit.rs` test and the `specs_coverage.rs`
      comment explaining why the misleading integration test was removed — acceptance: the test
      suite passes and the two files no longer differ from `beaver-nest`'s.

- [ ] [AI] **RED** — add regression tests at
      `apps/rhino-cli/src/application/env/validate.rs` proving F# keys passed to a pure
      `readEnvironment "KEY"` wrapper are detected and a direct
      `Environment.GetEnvironmentVariable("DOTNET_RUNNING_IN_CONTAINER")` read is excluded — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml scan_fsharp` — acceptance: both fail on
      canonical for their intended missing behavior, not because of fixture setup.

  **Gherkin (binds) →** "F# environment wrapper reads remain detectable after convergence"

  ```gherkin
  Scenario: F# environment wrapper reads remain detectable after convergence
    Given beaver-nest detects app-owned keys passed to a pure readEnvironment wrapper
    And it excludes the framework-owned DOTNET_RUNNING_IN_CONTAINER signal
    When Phase 11 upstreams the scanner into canonical
    Then canonical retains both behaviors with regression tests
    And the generic Gherkin scenario lands before any downstream copy
  ```

- [ ] [AI] **GREEN** — port the generic scanner behavior from `beaver-nest` into
      `apps/rhino-cli/src/application/env/validate.rs`, using synthetic fixture keys rather than a
      real repo's app names — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml scan_fsharp` — acceptance: both regressions pass and existing
      environment-scanner tests remain green.
- [ ] [AI] **REFACTOR** — port and genericize the corresponding coverage in
      `apps/rhino-cli/tests/env.rs` and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/env/env-validate-app-drift.feature` — commands:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test env` and
      `npx nx run rhino-cli:specs:behavior:coverage` — acceptance: both exit 0, fixtures name no real
      repo app, and the focused unit tests remain green.

- [ ] [AI] **RED** — add a regression test at `apps/rhino-cli/tests/cargo_target_share.rs` that reads
      `apps/rhino-cli/project.json` and proves every Rust test/coverage target clears inherited
      `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_COMMON_DIR` before invoking Cargo — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test cargo_target_share` — acceptance:
      fails on canonical because its three target commands clear none of them.

  **Gherkin (binds) →** "Rust test targets ignore inherited Git process state"

  ```gherkin
  Scenario: Rust test targets ignore inherited Git process state
    Given a rhino-cli test target is invoked with inherited GIT_DIR, GIT_WORK_TREE and GIT_COMMON_DIR
    When Nx launches the Rust test or coverage command
    Then all three inherited variables are cleared for that command
    And a regression test protects the target configuration before any downstream copy
  ```

- [ ] [AI] **GREEN** — prefix the `test:unit`, `test:integration`, and `test:coverage` commands in
      `apps/rhino-cli/project.json` with
      `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR`, matching the proven `beaver-nest` fix —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test cargo_target_share` —
      acceptance: the regression passes.
- [ ] [AI] **REFACTOR** — exercise the targets with poisoned inherited Git variables — command:
      `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent GIT_COMMON_DIR=/nonexistent npx nx run-many -t test:unit,test:integration -p rhino-cli`
      — acceptance: exits 0, temporary Git-fixture tests create and inspect only their own repos, and
      the focused regression remains green.

### 11.4 Close the live three-repo violation

- [ ] [AI] Adopt `zai-coding-plan/wrong` in `sync_validator.rs`'s
      `validate_agent_equivalence_fails_on_model_mismatch` fixture, matching `ose-primer` and
      `ose-private` — acceptance:
      `diff <(git show HEAD:apps/rhino-cli/src/application/agents/sync_validator.rs) apps/rhino-cli/src/application/agents/sync_validator.rs`
      shows exactly one changed line, and the model-mismatch test still **fails** on a mismatched
      model (verify by temporarily supplying a matching model and observing the test fail to fire).

### 11.5 Parity manifest and its gate

- [ ] [AI] **RED** — failing tests for `parity manifest generate` and `parity manifest validate` —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib parity` — acceptance:
      fails because the commands do not exist.

  **Gherkin (underpins) →** "An unannounced edit to byte-identical source fails the gate"; "The
  manifest never regenerates itself"; "The manifest covers tests/ as well as src/"; "Untracked
  files never enter the manifest"; "Regeneration is idempotent"

- [ ] [AI] **GREEN** — implement both. The boundary set is `apps/rhino-cli/src/**`,
      `apps/rhino-cli/tests/**`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/**`, enumerated via `git ls-files` so untracked
      files cannot enter — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — four properties, each needing its own test because each covers a direction
      the others do not: generation is idempotent (second run byte-identical); an edit to a `src/`
      file fails validation; an edit to a `tests/` file **also** fails validation; and an untracked
      file under `tests/fixtures/` is absent from the manifest and does not fail validation —
      acceptance: all four pass. The untracked case is not hypothetical: `ose-public`'s tree carries
      two untracked `.env` fixtures today, which must never be read, hashed, or listed.
- [ ] [AI] **RED** — add a failing test in the `parity` module asserting the `parity-manifest`
      failure message names the offending file, states it is byte-identical across all four repos,
      and names `parity manifest generate` as the deliberate remedy, per
      [tech-docs §2.8.4](./tech-docs.md#284-enforcement--a-hermetic-gate-plus-a-non-hermetic-audit)
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib parity` — acceptance:
      fails because the message does not yet contain all three required elements.

  **Gherkin (binds) →** "An unannounced edit to byte-identical source fails the gate"

  ```gherkin
  Scenario: An unannounced edit to byte-identical source fails the gate
    Given apps/rhino-cli/parity-manifest.sha256 is committed and current
    And a tracked file in the boundary set is edited
    When the gate with id "parity-manifest" runs
    Then it exits non-zero
    And the message names the file
    And the message states the file is byte-identical across all four repos
    And the message names "rhino-cli parity manifest generate" as the deliberate remedy
  ```

- [ ] [AI] **GREEN** — implement the failure message per
      [tech-docs §2.8.4](./tech-docs.md#284-enforcement--a-hermetic-gate-plus-a-non-hermetic-audit)
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib parity` — acceptance:
      the new test passes, no other tests broken.
- [ ] [AI] Declare the `parity-manifest` gate on `pre-push` and `ci`, and **confirm the generator is
      absent from every surface** — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.command=="parity manifest generate")] | length == 0'`
      exits 0. Verify the inverse: adding it to `pre-commit` makes that same command return false.
- [ ] [AI] **P1B-MANIFEST** — Generate the manifest and commit it — acceptance:
      `... -- parity manifest validate` exits 0, and re-running `generate` leaves the file unchanged.

### Phase 11 Execution-Ready Gate

- [ ] [AI] **P1B-READY** (`blockedBy: P1B-MANIFEST`; `blocks: P1B-LAND`) — command:
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: exits 0
      before any Phase 11 Land action begins, with the parity manifest present and valid.

### 11.6 Land

Every non-merge checkbox in this subsection is `blockedBy: P1B-READY`; the untagged protected merge
checkbox remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit Phase 11 — command: `git add -- apps/rhino-cli specs/apps/rhino repo-config.yml && git diff --cached --name-only -- apps/rhino-cli repo-config.yml | grep -q '^repo-config.yml$' && git commit -m 'refactor(rhino-cli): remove repository-specific source data'` — acceptance: commitlint and `npm run validate:sync` exit 0; the staged diff contains both the shared-source removal and its paired `repo-config.yml` extraction.
- [ ] [AI] Push Phase 11 — command: `git push -u origin sdlc-gate-registry-enforcement-defork` — acceptance: exits 0.
- [ ] [AI] Open its draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement-defork --fill` — acceptance: `gh pr view --json number,url` returns one PR.
- [ ] [AI] Cycle 1 maker fan-out — invoke all eight `pr-review-*-maker` disciplines — acceptance: eight reports exist.
- [ ] [AI] Cycle 1 synthesis — invoke `pr-review-synthesis-maker` — acceptance: one review of record is posted.
- [ ] [AI] Cycle 1 fixer — invoke `pr-review-fixer` — acceptance: accepted findings are fixed, committed, and pushed.
- [ ] [AI] Cycle 1 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-defork --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; otherwise fix all, commit, and push before Cycle 2.
- [ ] [AI] Cycle 2 maker fan-out — invoke all eight makers — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 2 synthesis — invoke `pr-review-synthesis-maker` — acceptance: a fresh review is posted.
- [ ] [AI] Cycle 2 fixer — invoke `pr-review-fixer` — acceptance: accepted findings are fixed, committed, and pushed.
- [ ] [AI] Cycle 2 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-defork --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; failures are fixed and pushed before Cycle 3.
- [ ] [AI] Cycle 3 maker fan-out — invoke all eight makers — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 3 synthesis — invoke `pr-review-synthesis-maker` — acceptance: a fresh review is posted.
- [ ] [AI] Cycle 3 fixer — invoke `pr-review-fixer` — acceptance: accepted findings are fixed, committed, and pushed.
- [ ] [AI] Cycle 3 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-defork --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; failures are fixed and pushed before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft is false and all five hardened preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 11 Gate

> These post-integration checks must pass before starting Phase 2. Canonical is technically copyable at this
> point, but Phases 3, 4, and 5 stay blocked until Phase 2 finalizes the governance files they also
> consume.

- [ ] [AI] Enumerated shared-data sites contain no real app names — acceptance:
      `rg -n "ayokoding|organiclever|ose-be|ose-www|wahidyankf" apps/rhino-cli/src/application/domain_coverage/mod.rs apps/rhino-cli/src/commands/specs_validate_counts.rs apps/rhino-cli/src/commands/specs_coverage.rs apps/rhino-cli/src/application/doctor/tools.rs`
      exits 1 with no match.
- [ ] [AI] `rhino-cli --help` output is unchanged from the Phase 1 baseline — acceptance:
      `diff /tmp/help-before.txt <(rhino-cli --help)` exits 0.
- [ ] [AI] `ROADMAP.md`/`SECURITY.md` are exempt in canonical — acceptance: `md naming validate`
      exits 0 on a `ROADMAP.md` fixture.
- [ ] [AI] F# environment-wrapper reads and framework-owned-key exclusion are preserved in canonical
      — acceptance: `cargo test --manifest-path apps/rhino-cli/Cargo.toml scan_fsharp` and
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test env` both exit 0.
- [ ] [AI] Rust test targets isolate inherited Git process state — acceptance:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test cargo_target_share` exits 0 and all
      three target commands in `project.json` clear `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_COMMON_DIR`.
- [ ] [AI] Parity manifest exists and validates — acceptance: `... -- parity manifest validate`
      exits 0.
- [ ] [AI] `nx run rhino-cli:test:quick` exits 0.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.

> **Pause Safety**: canonical source is de-forked, its manifest validates, all checks are green, and
> the four refs plus Phase 2 as the next node are recorded in the bounded transaction ledger. This
> controlled checkpoint is safe to stop, but not safe for unrelated boundary work or an
> identity-restored claim. To resume: run the four exact `rev-parse origin/main` commands in the
> transaction protocol, compare them with the ledger, validate the canonical parity manifest, and
> continue Phase 2. Phases 3–5 remain blocked until Phase 2 finalizes their governance documents.

---

## Phase 2 — Rewire and Retire `main-ci` (`ose-public`, PR #2)

Delivery unit: `ose-public`'s four surfaces derive from the registry, `main-ci.yml` is gone, and the
documents agree. This is the final canonical transaction checkpoint; downstream propagation remains
mandatory before the byte-identity invariant is restored.

- [ ] [AI] Create the Phase 2 worktree from the merged Phase 11 state — commands:
      `git fetch origin main` and
      `git worktree add -b sdlc-gate-registry-enforcement-rewire worktrees/sdlc-gate-registry-enforcement-rewire-public origin/main`
      — acceptance: the worktree is clean and `HEAD...origin/main` reports `0 0`.
- [ ] [AI] Install dependencies in the Phase 2 worktree — command:
      `npm --prefix worktrees/sdlc-gate-registry-enforcement-rewire-public install` — acceptance:
      exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd worktrees/sdlc-gate-registry-enforcement-rewire-public && npm run doctor -- --fix)` —
      acceptance: exits 0 and the follow-up doctor check reports no missing tool.

### 2.1 Populate the registry

- [ ] [AI] Copy the `gates:` section from
      [`repo-configs/repo-config-ose-public.yml`](./repo-configs/repo-config-ose-public.yml) into
      `repo-config.yml`. The target state is authored in this plan, not derived at execution time —
      acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate`
      exits 0, and
      `diff <(sed -n '/^gates:/,$p' repo-config.yml) <(sed -n '/^gates:/,$p' plans/in-progress/sdlc-gate-registry-enforcement/repo-configs/repo-config-ose-public.yml)`
      is empty. This uses the available shell tools and does not assume `yq` is installed.
- [ ] [AI] Confirm the registry covers every row of the audit table in
      [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today), with each check's
      current excludes preserved verbatim in `args.exclude` — acceptance: every audit-table command
      appears in `... -- gate list --format=json`, checked row by row with a per-row verdict rather
      than a single count comparison. A count match can hide one missing check offsetting one extra.
- [ ] [AI] Prune the one formatter entry `ose-public` declares for a language it does not track
      (Clojure) — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 13'`
      exits 0, and every surviving formatter's glob matches at least one path in `git ls-files`.
      Verify the inverse: the pre-edit registry fails that same glob-coverage check for exactly one
      entries.
- [ ] [AI] Verify the emitted `lint-staged` block matches the authored target — acceptance:
      `... -- gate emit --surface=pre-commit` then
      `diff <(jq '."lint-staged"' package.json) plans/in-progress/sdlc-gate-registry-enforcement/package-json/lint-staged-ose-public.json`
      is empty. This is the falsifiable test of the emitter, and it is a diff, not a judgement.
- [ ] [AI] Verify the whole `package.json` matches the authored target, not only the emitted block —
      acceptance:
      `diff package.json plans/in-progress/sdlc-gate-registry-enforcement/package-json/package-ose-public.json`
      is empty. Catches an accidental edit to a script, pin, or workspace glob that the
      `lint-staged`-only diff above cannot see.
- [ ] [AI] Verify the three rewritten hooks match the authored targets — command:
      `for h in commit-msg pre-commit pre-push; do diff ".husky/$h" "plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/$h-ose-public.sh" || exit 1; done`
      — acceptance: exits 0.
- [ ] [AI] Before overwriting, verify the three live hooks match the captured pre-change files —
      command:
      `for h in commit-msg pre-commit pre-push; do diff ".husky/$h" "plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/current/$h-ose-public" || exit 1; done`
      — acceptance: exits 0. A non-empty diff means someone else changed the hook after the
      2026-08-04 revalidation; reconcile it rather than overwriting.
- [ ] [AI] Declare `md-mermaid`, `md-heading-hierarchy`, and the structural specs validator on the
      `ci` surface — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("md-mermaid") != null and index("md-heading-hierarchy") != null'`
      exits 0. Verify the inverse holds before the edit: the same command returns false on the
      pre-edit registry.
- [ ] [AI] Declare `harness-bindings` on the `ci` surface (closes R-6) — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("harness-bindings") != null'`
      exits 0.
- [ ] [AI] Declare **every** formatter in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) as
      `type: mutation` on `pre-commit`, each paired with a `format-verify-*` `type: check` on `ci`
      only, linked by `verifies` (closes R-7) — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.type=="mutation" and .category=="formatter") | .id] - [.[] | select(.verifies) | .verifies] | length == 0'`
      exits 0 (no formatter lacks a verifier), and `... -- gate validate` exits 0. Verify the inverse
      before the edit: deleting one `verifies` field makes both non-zero. **Not** a single
      `format-verify` — one `prettier --check` leaves thirteen languages unverified.

  > **Why the Go and Elixir wrappers are built here, in a repo with zero `.go` and zero `.ex` files.**
  > `[Repo-grounded]` `git ls-files '*.go' '*.ex' '*.exs'` returns nothing in `ose-public`, yet
  > `scripts/format-elixir.sh` **is** tracked here — it is part of the shared toolchain, not of any one
  > repo's language set. Two different things are being placed, and only one of them is language-gated:
  > the wrapper **implementations** (the script's check mode, and the `rhino-cli` test asserting
  > wrapper semantics) are canonical-source artifacts and must land in `ose-public` under the
  > byte-identity boundary; the wrapper **gate declarations** are per-repo data and appear only in
  > `ose-primer`'s registry, the sole repo with tracked Go and Elixir files. Building the
  > implementation here and declaring the gate there is the presence rule working as designed, not a
  > misplacement.

- [ ] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/gate_format_verify_wrappers.rs`
      (_New file_) for the verify command that needs more than a flag: `gofmt -l` wrapped so
      non-empty output fails — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` —
      acceptance: fails because the wrapper does not exist yet. Fixture is synthetic (a temp
      unformatted `.go` file created by the test), since Go is not tracked here.

  **Gherkin (binds) →** "gofmt is wrapped because it cannot fail on its own"

  ```gherkin
  Scenario: gofmt is wrapped because it cannot fail on its own
    Given a tracked ".go" file is not formatted
    When the gate with id "format-verify-gofmt" runs
    Then it exits non-zero
    And the wrapper treats non-empty "gofmt -l" output as failure
  ```

- [ ] [AI] **GREEN** — implement the `gofmt -l` wrapper (non-empty output fails) — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` —
      acceptance: the new test passes: non-zero exit on a deliberately unformatted fixture, 0
      on a formatted one; no other tests broken.
- [ ] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/gate_format_verify_wrappers.rs` for
      `scripts/format-elixir.sh`'s new check mode (or a direct `mix format --check-formatted` call)
      on an unformatted fixture — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` —
      acceptance: fails because the check mode does not exist yet. Fixture is synthetic (a temp
      unformatted `.ex` file created by the test), since Elixir is not tracked here.

  **Gherkin (binds) →** "The Elixir formatter script gains a check mode that fails"

  ```gherkin
  Scenario: The Elixir formatter script gains a check mode that fails
    Given a tracked ".ex" file is not formatted
    When the gate with id "format-verify-elixir" runs
    Then it exits non-zero
    And no tracked file is rewritten
  ```

- [ ] [AI] **GREEN** — implement `scripts/format-elixir.sh`'s check mode so it exits non-zero on an
      unformatted fixture and rewrites no tracked file — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` — acceptance: the new
      test passes, no other tests broken.
- [ ] [AI] **RED** — add a failing test at `apps/rhino-cli/tests/gate_format_verify_wrappers.rs`:
      the same check mode exits zero and rewrites nothing when every tracked `.ex`/`.exs` fixture is
      already formatted — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` —
      acceptance: fails because the check mode does not yet distinguish the already-formatted case.

  **Gherkin (binds) →** "The Elixir check mode passes on formatted sources"

  ```gherkin
  Scenario: The Elixir check mode passes on formatted sources
    Given every tracked ".ex" and ".exs" file is formatted
    When the gate with id "format-verify-elixir" runs
    Then it exits zero
    And no tracked file is rewritten
  ```

- [ ] [AI] **GREEN** — confirm the check mode exits zero and rewrites nothing on an already-formatted
      fixture set — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_format_verify_wrappers` —
      acceptance: the new test passes, no other tests broken.
- [ ] [AI] Declare the remaining mutations — `harness-bindings-generate` and `lockfile-sync` — and
      the two surface-unique checks `env-staged-guard` (`carve-out: staged-only`) and `commitlint`
      (surface `commit-msg`) — acceptance: `... -- gate list --format=json | jq -e '[.[].id] | contains(["harness-bindings-generate","lockfile-sync","env-staged-guard","commitlint"])'`
      exits 0. This is the step that makes the registry a complete source of truth: after it, nothing
      any surface does lives outside `gates:`.
- [ ] [AI] Confirm `deps:audit` is **absent** from the registry — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.command=="deps:audit")] | length == 0'`
      exits 0. It is excluded by decision, not oversight; see
      [tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).
- [ ] [AI] Declare `test-quick` and `compat-min-version` with `wiring: hand-wired` — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("test-quick") == null'`
      exits 0 (absent from the matrix) **and** `... -- gate list --format=text` names it (present in
      the registry).

### 2.1a Dependency-audit workflow and its naming-convention amendment

Ordered — the convention must permit the name before the file can legally carry it.

- [ ] [AI] Amend `repo-governance/development/infra/github-actions-workflow-naming.md`: add
      `dependency` to the cross-cutting `{domain}` list and `audit` to the verb-and-qualifier
      vocabulary. Both checks below must be **row-scoped**: a bare `grep -c 'audit'` already returns
      1 today, matching the unrelated word "audits." in prose, so it would pass without the edit —
      acceptance, run from the repo root:

  ```sh
  F=repo-governance/development/infra/github-actions-workflow-naming.md
  grep -cF '| `audit`' "$F"                # 0 today, 1 after: the vocabulary row exists
  grep -cE '^\| .\{domain\}.*dependency' "$F"  # 0 today, 1 after: the domain list names it
  ```

- [ ] [AI] Register the new workflow in that convention's Cross-cutting workflows table — acceptance,
      from the repo root:

  ```sh
  F=repo-governance/development/infra/github-actions-workflow-naming.md
  grep -cF '| `dependency-vulnerability-audit.yml`' "$F"  # 0 today, 1 after
  grep -cF '| `pr-quality-gate.yml`' "$F"                 # 2 today and after (it also heads a
                                                          # column in the per-language table at :295)
  grep -cF '| `validate-env.yml`' "$F"                    # 1 today and after, untouched
  ```

  No `main-ci.yml` row is removed here: that table never listed it, so an earlier
  `grep -c 'main-ci' returns 0` clause was satisfied before any edit and proved nothing.

- [ ] [AI] Create `.github/workflows/dependency-vulnerability-audit.yml` with
      `name: Dependency Vulnerability Audit`, carrying over the existing `schedule` cron and
      `workflow_dispatch` triggers and the `nx run-many --all -t deps:audit` step verbatim, plus this
      repo's existing toolchain setup actions — acceptance: `actionlint .github/workflows/dependency-vulnerability-audit.yml`
      exits 0.
- [ ] [AI] Verify the name derives to the filename mechanically per the convention:
      `Dependency Vulnerability Audit` → lowercase → spaces to hyphens →
      `dependency-vulnerability-audit` → `.yml` — acceptance: derived string equals the filename
      exactly. This is the check `ose-primer` fails today with `Nightly Dependency Audit` in
      `deps-audit.yml`.
- [ ] [AI] `git rm .github/workflows/deps-audit.yml` — acceptance:
      `test ! -f .github/workflows/deps-audit.yml` and
      `test -f .github/workflows/dependency-vulnerability-audit.yml`. Do not delete before the
      replacement exists and lints — a window with neither workflow present means an unaudited night.
- [ ] [AI] Update `.github/workflows/README.md`: replace the `deps-audit.yml` row, drop the
      `main-ci.yml` row — acceptance: `grep -c 'deps-audit' .github/workflows/README.md` returns 0
      and `grep -c 'dependency-vulnerability-audit' .github/workflows/README.md` returns at least 1.

### 2.2 Rewire the hooks

- [ ] [AI] Run `... -- gate emit --surface=pre-commit` to generate the `lint-staged` block in
      `package.json` from the registry — acceptance: `git diff --stat package.json` shows the block
      changed.
- [ ] [AI] Validate the emitted block — command:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` —
      acceptance: exits 0 and reports the artifact fresh.
- [ ] [AI] Inverse/idempotence check — command:
      `cp package.json /tmp/package-after-emit.json && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate emit --surface=pre-commit && diff /tmp/package-after-emit.json package.json`
      — acceptance: exits 0 and `grep -c '"lint-staged"' package.json` prints `1`.
- [ ] [AI] Replace the check list in `.husky/pre-commit` with `gate run --surface=pre-commit`, which
      now drives the mutations too (they are declared, so the hook no longer names them) —
      acceptance: `bash .husky/pre-commit` on a staged no-op exits 0; and
      `grep -c 'gate run --surface=pre-commit' .husky/pre-commit` returns 1.
- [ ] [AI] Replace the check list in `.husky/pre-push` with `gate run --surface=pre-push` —
      acceptance: `grep -c 'gate run --surface=pre-push' .husky/pre-push` returns 1; and
      `grep -cE 'md links validate|md readme-index validate|harness duplication validate' .husky/pre-push`
      returns 0 (they now come from the registry, not the hook text).
- [ ] [AI] Verify no check was dropped in the move: compare
      `... -- gate list --surface=pre-push --format=json` against the pre-edit `.husky/pre-push`
      command list recorded in Phase 0 — acceptance: every pre-edit command appears in the registry
      projection; any deliberate omission is listed here with its reason.

### 2.3 Rewire the PR gate

- [ ] [AI] Replace the hand-listed check jobs in `.github/workflows/pr-quality-gate.yml` with the
      `enumerate` plus `gate` matrix from
      [tech-docs §2.5](./tech-docs.md#25-ci-wiring--matrix-not-a-single-job); keep the per-language
      `test:quick` jobs hand-written — acceptance: `actionlint .github/workflows/pr-quality-gate.yml`
      exits 0.
- [ ] [AI] Unpin the specs job (closes R-5): remove `--projects=rhino-cli` — acceptance:
      `grep -c -- '--projects=rhino-cli' .github/workflows/pr-quality-gate.yml` returns 0; it
      returned 1 before the edit.
- [ ] [AI] Remove `if: github.event_name == 'pull_request'` from the `format` job so the per-file
      pass also runs on push to `main`, and split it: auto-fix-and-commit on `pull_request`, verify-only
      on `push` — acceptance: `actionlint` exits 0; the `push` path runs `format-verify` and performs
      no `git push`.
- [ ] [AI] Update the `quality-gate` join job's `needs:` to depend on the matrix job, removing the 17
      hand-listed job names it replaces (`.github/workflows/pr-quality-gate.yml:279-297`, verified by
      count). **This is the real hazard of the rewire**, not the branch
      protection: the join job is `if: always()` and fails only on
      `contains(needs.*.result, 'failure')`, so a `needs:` list that omits the matrix job reports
      green while checking nothing — acceptance: `actionlint .github/workflows/pr-quality-gate.yml`
      exits 0. Keep the job's `name: Quality gate` byte-identical.
- [ ] [AI] Verify the join dependency — introduce one deliberately failing matrix fixture on a
      scratch branch and run the workflow — acceptance:
      `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-rewire --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion`
      reports the `quality-gate` failure; revert the fixture before continuing.
- [ ] [AI] Verify the inverse once — remove the matrix job from `needs:` only on the scratch branch
      and rerun the same failing fixture — acceptance: the join incorrectly stays green, proving the
      test detects the hazard; restore `needs:`, rerun `actionlint`, and leave no scratch diff.

### 2.4 Retire `main-ci.yml`

Ordered — do not delete before the fold-in is verified.

- [ ] [AI] Confirm the fold-in landed: every command in `main-ci.yml` is either declared on the `ci`
      surface or deliberately dropped with a reason recorded here — acceptance: a per-command table
      appears in this checklist with a verdict for each; no command is unaccounted for.
- [ ] [AI] `git rm .github/workflows/main-ci.yml` — acceptance:
      `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Scrub references from the **live** surfaces — the four tracked files that describe CI as it
      currently works — acceptance:
      `git ls-files -z | xargs -0 grep -l "main-ci" | grep -E '^(\.github/workflows/|docs/reference/|repo-governance/)'`
      returns nothing. Today it returns six paths:
      `.github/workflows/README.md`, `.github/workflows/main-ci.yml` (deleted by the step above),
      `.github/workflows/pr-quality-gate.yml`, `docs/reference/sdlc-gate-standard.md`,
      `docs/reference/system-architecture/ci-cd.md`, and
      `repo-governance/development/infra/nx-targets.md`.
- [ ] [AI] Leave the **narrative** references alone — acceptance: after the scrub,
      `git ls-files -z | xargs -0 grep -l "main-ci"` still returns matches, and every one of them
      falls in exactly these six categories:

  ```sh
  # Every surviving path must match one of these prefixes. Anything else is a missed live surface.
  git ls-files -z | xargs -0 grep -l "main-ci" \
    | grep -vE '^(plans/done/|plans/backlog/|plans/ideas/|plans/in-progress/README\.md$|plans/in-progress/sdlc-gate-registry-enforcement/|apps/ose-www/content/updates/)'
  ```

  Returns nothing once the six live surfaces are scrubbed. Note the fifth and sixth categories:
  `plans/in-progress/README.md` and, separately, **this plan's own folder**, which discusses
  `main-ci.yml` throughout — it is the plan's subject — so the plan's documents are themselves
  narrative references and must not be scrubbed. Omitting the plan's-own-folder category from the
  enumeration was an earlier defect in this step. These are history, future-work notes, and this
  plan's own record; rewriting them would falsify it. A repo-wide "no match anywhere" clause is
  **unsatisfiable** and was the original form of this step.

### 2.5 Documents

- [ ] [AI] Amend `docs/reference/sdlc-gate-standard.md` per
      [tech-docs §3](./tech-docs.md#3-document-amendments) — acceptance:
      `grep -c 'pre-commit ∪ pre-push) == PR gate == main gate' docs/reference/sdlc-gate-standard.md`
      returns 0 and `grep -c 'pre-commit ∪ pre-push) == PR gate' docs/reference/sdlc-gate-standard.md`
      returns at least 1.
- [ ] [AI] Rewrite `repo-governance/development/workflow/git-hook-lifecycle.md` (closes R-9) —
      acceptance: `grep -c 'specs:coverage' repo-governance/development/workflow/git-hook-lifecycle.md`
      returns 0; it returned at least 1 before the edit. Its command tables are replaced by a pointer
      to `gate list` so the document cannot restale.
- [ ] [AI] Update `repo-governance/development/infra/nx-targets.md`,
      `docs/reference/system-architecture/ci-cd.md`, and the Git Hooks section of `AGENTS.md` —
      acceptance: `npx nx run rhino-cli:instruction-size:validation` exits 0 (the `AGENTS.md` edit
      must not push it over budget).
- [ ] [AI] Propagate the rule change through `repo-rules-maker` rather than hand-editing only the
      obvious files: sweep the convention registers, the checker agents, and the indexes, then
      re-sync bindings — acceptance: `npm run validate:sync` exits 0 and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0.
- [ ] [AI] Extend the three-repo byte-identity language to four repos in
      `repo-governance/workflows/plan/multi-plans-execution.md` per
      [tech-docs §3](./tech-docs.md#3-document-amendments). This file does **not** use the phrase
      "across all three repos" — it enumerates the repos inline — so its acceptance clause must
      target its own wording. Assert the **new** language arrived rather than the old one vanished —
      a disappearance clause is satisfied by text that was never there — acceptance:
      `grep -c 'beaver-nest' repo-governance/workflows/plan/multi-plans-execution.md` returns
      non-zero, and
      `grep -cF 'All three edit' repo-governance/workflows/plan/multi-plans-execution.md` returns 0.
      Verify the inverse before the edit: they return 0 and 1 respectively today, so both flip.
- [ ] [AI] Extend the same language in
      `repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md` and
      `repo-governance/workflows/plan/plan-multi-repo-parity-planning.md` — acceptance:
      `grep -cF 'across all three repos' repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md repo-governance/workflows/plan/plan-multi-repo-parity-planning.md`
      returns 0 for each file, **and**
      `grep -c 'beaver-nest' repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md repo-governance/workflows/plan/plan-multi-repo-parity-planning.md`
      returns non-zero for each. Both file arguments are required — a bare `grep -c` reads stdin and
      reports on nothing. Verify the inverse: today they return 1 and 0 respectively, so both flip.
      Unlike
      `multi-plans-execution.md`, these two do carry the literal phrase, so the disappearance half is
      non-vacuous here — the arrival half is still required, because deleting the sentence would
      satisfy disappearance alone.
- [ ] [AI] Replace `plan-multi-repo-parity-planning.md`'s manual
      `git -C ose-public ls-files ... | xargs md5` diff snippet with a pointer to
      `... -- parity manifest validate` — acceptance:
      `grep -c 'xargs md5' repo-governance/workflows/plan/plan-multi-repo-parity-planning.md` returns 0.

### 2.5a Harness-Neutrality Verification

- [ ] [AI] **P2-HN-1** (`blockedBy: P2-DOCS`; `blocks: P2-HN-2`) — prove no secondary harness
      binding was hand-edited before generation. Run
      `git diff --exit-code -- .opencode/ .cursor/ .amazonq/` from
      `worktrees/sdlc-gate-registry-enforcement-rewire-public/` — acceptance: exits 0; any diff is
      reconciled to its `.claude/` source before continuing rather than edited in the secondary
      directory.
- [ ] [AI] **P2-HN-2** (`blockedBy: P2-HN-1`; `blocks: P2-HN-3`) — scan vendor-neutral governance
      with
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance vendor validate repo-governance/`
      — acceptance: exits 0 with `GOVERNANCE VENDOR AUDIT PASSED`; vendor-specific examples remain
      only under explicitly named `Platform Binding Examples` sections.
- [ ] [AI] **P2-HN-3** (`blockedBy: P2-HN-2`; `blocks: P2-HN-4`) — regenerate bindings only from
      canonical `.claude/` sources with `npm run generate:bindings && git add -- .claude .opencode .cursor .amazonq`
      — acceptance: both commands exit 0; every changed `.opencode/`, `.cursor/`, or `.amazonq/`
      path is generated output, is added to the same file-touch ledger and staged with its source,
      and remains staged for the Phase 2 commit.
- [ ] [AI] **P2-HN-4** (`blockedBy: P2-HN-3`; `blocks: P2-READY`) — run
      `npm run validate:sync` — acceptance: exits 0 and reports no source/mirror divergence; static
      inspection of generated files alone does not satisfy this gate.

### Phase 2 Execution-Ready Gate

- [ ] [AI] **P2-READY** (`blockedBy: P2-HN-4`; `blocks: P2-LAND`) — commands:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` and
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: both exit
      0 before any Phase 2 Land action begins.

### 2.6 Land

Every non-merge checkbox in this subsection is `blockedBy: P2-READY`; the untagged protected merge
checkbox remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] `... -- gate validate` exits 0 — this is the plan's central acceptance criterion.
- [ ] [AI] Commit Phase 2 — command: `git add -- .husky .github .claude .opencode .cursor .amazonq package.json repo-config.yml AGENTS.md scripts/format-elixir.sh docs repo-governance && git diff --cached --name-only -- scripts/format-elixir.sh | grep -qx 'scripts/format-elixir.sh' && git commit -m 'feat(ci): derive quality surfaces from gate registry'` — acceptance: commitlint and `npm run validate:sync` exit 0; the formatter wrapper and any generated binding source/mirror paths are staged in this same commit.
- [ ] [AI] Push Phase 2 — command: `git push -u origin sdlc-gate-registry-enforcement-rewire` — acceptance: exits 0.
- [ ] [AI] Open its draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement-rewire --fill` — acceptance: one PR URL is returned.
- [ ] [AI] Cycle 1 maker fan-out — invoke all eight makers — acceptance: eight reports exist.
- [ ] [AI] Cycle 1 synthesis — invoke `pr-review-synthesis-maker` — acceptance: one review is posted.
- [ ] [AI] Cycle 1 fixer — invoke `pr-review-fixer` — acceptance: fixes are committed and pushed.
- [ ] [AI] Cycle 1 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-rewire --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; otherwise fix, commit, push before Cycle 2.
- [ ] [AI] Cycle 2 maker fan-out — invoke all eight makers — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 2 synthesis — invoke synthesis maker — acceptance: one fresh review is posted.
- [ ] [AI] Cycle 2 fixer — invoke fixer — acceptance: fixes are committed and pushed.
- [ ] [AI] Cycle 2 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-rewire --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix and push before Cycle 3 on failure.
- [ ] [AI] Cycle 3 maker fan-out — invoke all eight makers — acceptance: eight fresh reports exist.
- [ ] [AI] Cycle 3 synthesis — invoke synthesis maker — acceptance: one fresh review is posted.
- [ ] [AI] Cycle 3 fixer — invoke fixer — acceptance: fixes are committed and pushed.
- [ ] [AI] Cycle 3 CI gate — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-rewire --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix and push before readiness on failure.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft is false and five preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 2 Gate

> These post-integration checks must pass before starting Phases 3, 4, and 5. Those sibling nodes fan out only
> after this gate; Phase 6 remains blocked until all three finish.

- [ ] [AI] `... -- gate validate` exits 0 in `ose-public`.
- [ ] [AI] `main-ci.yml` absent and unreferenced outside immutable history — acceptance:
      `test ! -f .github/workflows/main-ci.yml` exits 0.
- [ ] [AI] Accessible branch protection still resolves without reconfiguration — acceptance: the
      `Quality gate` context remains attached to the preserved join-job name; unprotected or
      unavailable repositories remain recorded as such rather than modified by this phase.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.

- [ ] [AI] Verify the canonical downstream source worktree — command:
      `git -C /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public status --porcelain && git -C /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public rev-list --left-right --count HEAD...origin/main`
      — acceptance: status is empty and the ref count is `0 0`; Phases 3–5 copy only from this
      attached, merged canonical path and never from the bare root.

> **Pause Safety**: `ose-public`'s hooks and CI derive from the registry; `main-ci.yml` is gone; the
> merge is on `main`. Safe to stop. To resume: `... -- gate validate` to confirm the merged state
> still passes, then start Phase 6 once Phases 3, 4, and 5 also merge.

---

## Phase 3 — `ose-primer` (PR #3)

Blocked by Phase 2; independent of Phases 4 and 5. Establishes the legacy tri-repo subset in parallel
with those nodes; it does not close the all-four target by itself.

- [ ] [AI] Create the declared `ose-primer` worktree from finalized Phase 2 `origin/main` — commands:
      `git -C /Users/wkf/ose-projects/ose-primer fetch origin main` and
      `git -C /Users/wkf/ose-projects/ose-primer worktree add -b sdlc-gate-registry-enforcement worktrees/sdlc-gate-registry-enforcement origin/main`
      — acceptance: the worktree is clean and `HEAD...origin/main` reports `0 0`.
- [ ] [AI] Install its dependencies — command:
      `npm --prefix /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement install` —
      acceptance: exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement && npm run doctor -- --fix)`
      — acceptance: exits 0 and a subsequent doctor check reports no missing tool. The polyglot demo
      apps require their language toolchains before pre-push can pass in a fresh worktree.
- [ ] [AI] Copy `apps/rhino-cli` from merged canonical — command:
      `rsync -a --delete /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/ /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement/apps/rhino-cli/` — acceptance:
      `src/`, `tests/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`,
      `parity-manifest.sha256` and `specs/apps/rhino/behavior/rhino-cli/gherkin/` are byte-identical
      to `ose-public`, verified by `diff -r`, and `... -- parity manifest validate` exits 0 against
      the copied manifest without regenerating it. Copying from the Phase 1 result instead would
      reintroduce the hardcoded app names Phase 11 removed.
- [ ] [AI] Copy the boundary Gherkin tree — command:
      `rsync -a --delete /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/specs/apps/rhino/behavior/rhino-cli/gherkin/ /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement/specs/apps/rhino/behavior/rhino-cli/gherkin/`
      — acceptance: `diff -r /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/specs/apps/rhino/behavior/rhino-cli/gherkin /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement/specs/apps/rhino/behavior/rhino-cli/gherkin` exits 0.
- [ ] [AI] Author `ose-primer`'s `gates:` section, preserving its own excludes (its `md links validate`
      carries the polyglot `deps`/`build`/`target` excludes) and adding its per-language gates —
      acceptance: `... -- repo-config validate` exits 0.
- [ ] [AI] Add the `shfmt -w` mutation and its `shfmt -d` verifier (8 tracked `.sh` files,
      `shellcheck`-ed but never formatted), and add prettier globs for the 46 tracked `.sql` and 3
      tracked `.html` files no glob currently covers — acceptance:
      `... -- gate list --format=json | jq -e '[.[].id] | index("format-shfmt") != null'` exits 0,
      and every tracked file extension in `git ls-files` that has a formatter in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) is matched by
      exactly one glob.
- [ ] [AI] Confirm no formatter is pruned here. `ose-primer` is the polyglot repo and is the **only**
      repo tracking Go, Elixir, C#, Clojure, and Dart — acceptance: every `category: formatter`
      gate's glob matches at least one path in `git ls-files`, with zero entries removed. The two
      formatters needing wrapper work — `gofmt` (prints paths, exits 0) and the Elixir script (no
      check mode) — are `ose-primer`-only, so that work lands here and nowhere else.
- [ ] [AI] **P3-CONFIG-COPY** — install the authored registry without its audit banner — command:
      `sed -n '/^# repo-config.yml — schema:/,$p' /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/repo-configs/repo-config-ose-primer.yml > /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement/repo-config.yml`
      — acceptance: `npm exec nx -- run rhino-cli:repo-config-validation` exits 0.
- [ ] [AI] **P3-PACKAGE-COPY** — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/package-json/package-ose-primer.json /Users/wkf/ose-projects/ose-primer/worktrees/sdlc-gate-registry-enforcement/package.json`
      — acceptance: `jq empty package.json` exits 0.
- [ ] [AI] **P3-HOOK-COMMIT-MSG** — copy `husky-hooks/commit-msg-ose-primer.sh` to `.husky/commit-msg` — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/commit-msg-ose-primer.sh .husky/commit-msg` — acceptance: `sh -n .husky/commit-msg` exits 0.
- [ ] [AI] **P3-HOOK-PRE-COMMIT** — command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-commit-ose-primer.sh .husky/pre-commit` — acceptance: `sh -n .husky/pre-commit` exits 0.
- [ ] [AI] **P3-HOOK-PRE-PUSH** — command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-push-ose-primer.sh .husky/pre-push` — acceptance: `sh -n .husky/pre-push` exits 0.
- [ ] [AI] **P3-PR-WORKFLOW** — replace the hand-written gate list in
      `.github/workflows/pr-quality-gate.yml` with enumerate/matrix jobs while preserving primer's
      exact toolchain setup jobs and `name: Quality gate` join job — command:
      `actionlint .github/workflows/pr-quality-gate.yml` — acceptance: exits 0 and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` exits 0.
- [ ] [AI] **P3-MAIN-CI-DELETE** — command: `git rm .github/workflows/main-ci.yml` — acceptance:
      `test ! -f .github/workflows/main-ci.yml` exits 0.
- [ ] [AI] **P3-DEPS-RENAME** — create `.github/workflows/dependency-vulnerability-audit.yml`
      (**new file**) from the finalized public workflow, then delete `.github/workflows/deps-audit.yml` — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/.github/workflows/dependency-vulnerability-audit.yml .github/workflows/dependency-vulnerability-audit.yml && git rm .github/workflows/deps-audit.yml`
      — acceptance: `actionlint .github/workflows/dependency-vulnerability-audit.yml` exits 0 and
      the new `name:` matches its filename. This repo is the one that also fixes a
      standing convention violation — it ships `name: Nightly Dependency Audit` inside a file named
      `deps-audit.yml`, which the `name:`-mirrors-filename rule forbids.
- [ ] [AI] Copy the amended `docs/reference/sdlc-gate-standard.md` — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/docs/reference/sdlc-gate-standard.md docs/reference/sdlc-gate-standard.md`
      — acceptance: `npm run lint:md` exits 0.
- [ ] [AI] **P3-PROPAGATION** — Copy rewritten `repo-governance/development/workflow/git-hook-lifecycle.md` — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/repo-governance/development/workflow/git-hook-lifecycle.md repo-governance/development/workflow/git-hook-lifecycle.md`
      — acceptance: `grep -c 'validate-markdown.yml' repo-governance/development/workflow/git-hook-lifecycle.md`
      returns 0 (this repo's copy cites that non-existent workflow today).

### Phase 3 Execution-Ready Gate

- [ ] [AI] **P3-READY** (`blockedBy: P3-PROPAGATION`; `blocks: P3-LAND`) — commands:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` and
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: both exit
      0 before any Phase 3 Land action begins.

Every non-merge Land checkbox below is `blockedBy: P3-READY`; the untagged protected merge checkbox
remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit Phase 3 — command: `git add -- apps/rhino-cli .husky .github package.json repo-config.yml docs repo-governance && git commit -m 'feat(ci): propagate registry gates to ose-primer'` — acceptance: commitlint and sync validation exit 0.
- [ ] [AI] Push Phase 3 — command: `git push -u origin sdlc-gate-registry-enforcement` — acceptance: exits 0.
- [ ] [AI] Open draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement --fill` — acceptance: one PR exists.
- [ ] [AI] Cycle 1 makers — invoke eight makers — acceptance: eight reports.
- [ ] [AI] Cycle 1 synthesis — invoke synthesis maker — acceptance: one posted review.
- [ ] [AI] Cycle 1 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 1 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix, commit, push before Cycle 2 on failure.
- [ ] [AI] Cycle 2 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 2 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 2 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 2 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before Cycle 3.
- [ ] [AI] Cycle 3 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 3 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 3 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 3 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft false and five preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 3 Gate

> All checks below must pass before starting Phase 6 (Phase 3 is blocked by Phase 2, independent of
> Phases 4 and 5, and one of three nodes that block Phase 6).

- [ ] [AI] `... -- gate validate` exits 0 in `ose-primer`.
- [ ] [AI] `apps/rhino-cli` byte-identical to `ose-public`'s Phase 11 result — acceptance: `diff -r`
      over the boundary set reports zero differences.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.

> **Pause Safety**: `ose-primer`'s hooks and CI derive from the registry; `apps/rhino-cli` matches
> canonical; the merge is on `main`. Safe to stop. To resume: `... -- gate validate` to confirm the
> merged state still passes, then start Phase 6 once Phases 4 and 5 also merge.

---

## Phase 4 — `ose-private` (PR #4)

Blocked by Phase 2; independent of Phases 3 and 5. Converges the legacy tri-repo subset, while
all-four closure still depends on Phase 5.

- [ ] [AI] Create the declared `ose-private` worktree — commands:
      `git -C /Users/wkf/ose-projects/ose-private fetch origin main` and
      `git -C /Users/wkf/ose-projects/ose-private worktree add -b sdlc-gate-registry-enforcement worktrees/sdlc-gate-registry-enforcement origin/main`
      — acceptance: the worktree is clean and `HEAD...origin/main` reports `0 0`.
- [ ] [AI] Install its dependencies — command:
      `npm --prefix /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement install` —
      acceptance: exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement && npm run doctor -- --fix)`
      — acceptance: exits 0 and a subsequent doctor check reports no missing tool.
- [ ] [AI] Copy canonical `apps/rhino-cli` — command:
      `rsync -a --delete /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/ /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/apps/rhino-cli/` — acceptance:
      `diff -r` reports no difference across the byte-identity file set (now including `tests/` and
      `parity-manifest.sha256`), and `... -- parity manifest validate` exits 0 without regenerating.
- [ ] [AI] **P4-REGISTRY-AUTHORING** — Author `ose-private`'s `gates:` section. It carries entries the others do not — the
      `iac-lint` pair (`./scripts/lint-terraform.sh`, `yamllint`) at pre-commit, pre-push, and CI —
      acceptance: `... -- repo-config validate` exits 0 and `... -- gate validate` exits 0, proving
      the schema tolerates a repo-specific entry set.
- [ ] [AI] Migrate the inline IaC formatting out of `.husky/pre-commit`. This repo currently formats
      `.tf` files by invoking the HashiCorp `terraform` binary (`terraform fmt -check -recursive
infra/on-premise/terraform/`) through a hand-written hook block rather than `lint-staged`, so
      `gate emit` reading the per-file registry would not reproduce it and the completeness claim
      would be false here on day one. This step deliberately standardizes on `tofu fmt` instead,
      matching `ose-public`'s existing choice. `[Web-cited]` OpenTofu's official
      [migration overview](https://opentofu.org/docs/intro/migration/) (accessed 2026-08-04) says it
      aims for Terraform-configuration compatibility and most code works unchanged, but still
      requires verification. Phase 0 provisions `tofu`; declare it as
      an ordinary `scope: affected-file-type, glob: "*.tf"` mutation with
      `category: formatter` plus its `format-verify-*` counterpart, then delete the inline block —
      acceptance: `grep -c 'fmt' .husky/pre-commit` returns 0, and
      `... -- gate list --surface=pre-commit --format=json | jq -e '[.[] | select(.surfaces."pre-commit".glob=="*.tf")] | length == 1'`
      exits 0. Verify the inverse first: the same `jq` returns false on the pre-edit registry.
- [ ] [AI] Add the `shfmt -w` mutation and its `shfmt -d` verifier (13 tracked `.sh` files,
      `shellcheck`-ed but never formatted) — acceptance:
      `... -- gate list --format=json | jq -e '[.[].id] | index("format-shfmt") != null'` exits 0.
- [ ] [AI] Prune the five formatter entries this repo declares for languages it does not track — F#,
      Python, C#, Clojure, Dart are all **zero** tracked files here — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 4'`
      exits 0 (prettier, rustfmt, shfmt, tofu — the four it actually needs).
- [ ] [AI] Note the pre-existing local surplus: this repo's pre-push already runs
      `specs structure validate` and `npm run lint:md`, and its PR gate already has
      `markdown-per-file`. Fold these into registry declarations rather than deleting them —
      acceptance: every command present in the pre-edit `.husky/pre-push` appears in
      `... -- gate list --surface=pre-push --format=json`.
- [ ] [AI] **P4-CONFIG-COPY** (`blockedBy: P4-REGISTRY-AUTHORING`; `blocks: P4-PACKAGE-COPY`) —
      install the authored registry without its audit banner — command:
      `sed -n '/^# repo-config.yml — schema:/,$p' /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/repo-configs/repo-config-ose-private.yml > /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/repo-config.yml`
      — acceptance: `(cd /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement && npm exec nx -- run rhino-cli:repo-config-validation)` exits 0.
- [ ] [AI] **P4-PACKAGE-COPY** (`blockedBy: P4-CONFIG-COPY`; `blocks: P4-HOOK-COMMIT-MSG`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/package-json/package-ose-private.json /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/package.json`
      — acceptance: `jq empty /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/package.json` exits 0.
- [ ] [AI] **P4-HOOK-COMMIT-MSG** (`blockedBy: P4-PACKAGE-COPY`; `blocks: P4-HOOK-PRE-COMMIT`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/commit-msg-ose-private.sh /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/commit-msg`
      — acceptance: `sh -n /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/commit-msg` exits 0.
- [ ] [AI] **P4-HOOK-PRE-COMMIT** (`blockedBy: P4-HOOK-COMMIT-MSG`; `blocks: P4-HOOK-PRE-PUSH`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-commit-ose-private.sh /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/pre-commit`
      — acceptance: `sh -n /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/pre-commit` exits 0.
- [ ] [AI] **P4-HOOK-PRE-PUSH** (`blockedBy: P4-HOOK-PRE-COMMIT`; `blocks: P4-PR-WORKFLOW`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-push-ose-private.sh /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/pre-push`
      — acceptance: `sh -n /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.husky/pre-push` exits 0.
- [ ] [AI] **P4-PR-WORKFLOW** (`blockedBy: P4-HOOK-PRE-PUSH`; `blocks: P4-DEPS-COPY`) — replace
      the hand-written gate list in the exact destination
      `/Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/pr-quality-gate.yml`
      with enumerate/matrix jobs while preserving private's toolchain setup and `name: Quality gate`
      join job — acceptance: `actionlint /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/pr-quality-gate.yml` exits 0.
- [ ] [AI] **P4-DEPS-COPY** (`blockedBy: P4-PR-WORKFLOW`; `blocks: P4-DEPS-DELETE`) — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/.github/workflows/dependency-vulnerability-audit.yml /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/dependency-vulnerability-audit.yml`
      — acceptance: `actionlint /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/dependency-vulnerability-audit.yml` exits 0.
- [ ] [AI] **P4-DEPS-DELETE** (`blockedBy: P4-DEPS-COPY`; `blocks: P4-PARITY-WORKFLOW`) — command:
      `git -C /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement rm .github/workflows/deps-audit.yml`
      — acceptance: `test ! -f /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/deps-audit.yml` exits 0.
- [ ] [AI] **P4-PARITY-WORKFLOW** (`blockedBy: P4-DEPS-DELETE`; `blocks: P4-MAIN-CI-DELETE`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/.github/workflows/rhino-cli-parity-audit.yml /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/rhino-cli-parity-audit.yml`
      — acceptance: `actionlint /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/rhino-cli-parity-audit.yml` exits 0.
- [ ] [AI] **P4-MAIN-CI-DELETE** (`blockedBy: P4-PARITY-WORKFLOW`; `blocks: P4-DOCS`) — command:
      `git -C /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement rm .github/workflows/main-ci.yml`
      — acceptance: `test ! -f /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/.github/workflows/main-ci.yml` exits 0.
- [ ] [AI] Create `repo-governance/development/workflow/git-hook-lifecycle.md`, which this repo lacks
      entirely — acceptance: the file exists and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0 (the new file must be indexed).
- [ ] [AI] **P4-PROPAGATION** — Copy the finalized amended SDLC standard — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/docs/reference/sdlc-gate-standard.md /Users/wkf/ose-projects/ose-private/worktrees/sdlc-gate-registry-enforcement/docs/reference/sdlc-gate-standard.md`
      — acceptance: `npm run lint:md` exits 0 from the private worktree.

### Phase 4 Execution-Ready Gate

- [ ] [AI] **P4-READY** (`blockedBy: P4-PROPAGATION`; `blocks: P4-LAND`) — commands:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` and
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: both exit
      0 before any Phase 4 Land action begins.

Every non-merge Land checkbox below is `blockedBy: P4-READY`; the untagged protected merge checkbox
remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit Phase 4 — command: `git add -- apps/rhino-cli .husky .github package.json repo-config.yml docs repo-governance && git commit -m 'feat(ci): propagate registry gates to ose-private'` — acceptance: commitlint and sync validation exit 0.
- [ ] [AI] Push Phase 4 — command: `git push -u origin sdlc-gate-registry-enforcement` — acceptance: exits 0.
- [ ] [AI] Open draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement --fill` — acceptance: one PR exists.
- [ ] [AI] Cycle 1 makers — invoke eight makers — acceptance: eight reports.
- [ ] [AI] Cycle 1 synthesis — invoke synthesis maker — acceptance: one posted review.
- [ ] [AI] Cycle 1 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 1 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix, commit, push before Cycle 2.
- [ ] [AI] Cycle 2 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 2 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 2 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 2 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before Cycle 3.
- [ ] [AI] Cycle 3 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 3 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 3 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 3 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft false and five preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 4 Gate

> All checks below must pass before starting Phase 6 (Phase 4 is blocked by Phase 2, independent of
> Phases 3 and 5, and one of three nodes that block Phase 6). A green gate converges the legacy
> three-repo subset; the all-four byte-identity window closes only when Phase 5 is also green.

- [ ] [AI] `... -- gate validate` exits 0 in `ose-private`.
- [ ] [AI] `apps/rhino-cli` byte-identical across all three bound repos (`ose-public`, `ose-primer`,
      `ose-private`) — acceptance: `diff -r` over the boundary set reports zero differences for every
      pair.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.

> **Pause Safety**: `ose-private`'s hooks and CI derive from the registry; the legacy three-repo
> subset matches; the merge is on `main`. Safe to stop. To resume: `... -- gate validate` to confirm
> the merged state still passes, then start Phase 6 once Phases 3 and 5 also merge.

---

## Phase 5 — `beaver-nest` Joins the Byte-Identity Boundary (PR #5)

Blocked by Phase 2; independent of Phases 3 and 4.

`beaver-nest` **stops being a fork**. Phase 11 removes the defects that forced the fork and upstreams
the capabilities that accumulated there: eight of ten source divergences are repo-specific data or
fixtures hardcoded into shared source; the other two are the `ROADMAP.md`/`SECURITY.md` naming
exemptions and F# environment-wrapper detection. Phase 11 also absorbs the fork's inherited-Git-state
isolation in `project.json`, its corresponding integration tests, and its Gherkin coverage. This
therefore becomes a copy like Phases 3 and 4, not a port. See
[tech-docs §2.8.6](./tech-docs.md#286-the-governance-change-this-requires) for the governance
amendment this depends on.

- [ ] [AI] Fetch current `origin/main` from the bare repo root — command:
      `git -C /Users/wkf/ose-projects/beaver-nest fetch origin main` — acceptance: exits 0 and updates
      `refs/remotes/origin/main`.
- [ ] [AI] Create the declared attached worktree — command:
      `git -C /Users/wkf/ose-projects/beaver-nest worktree add -b sdlc-gate-registry-enforcement worktrees/sdlc-gate-registry-enforcement origin/main`
      — acceptance: it is on the named branch, clean, level with `origin/main`, and unrelated
      worktrees are unchanged.
- [ ] [AI] Install its dependencies — command:
      `npm --prefix /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement install` —
      acceptance: exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement && npm run doctor -- --fix)`
      — acceptance: exits 0 and a subsequent doctor check reports no missing tool.
- [ ] [AI] **Verify Phase 11 actually absorbed the fork before overwriting anything.** Diff the
      current `beaver-nest` source against merged canonical and confirm every remaining difference is
      one Phase 11 intended to erase — acceptance: `diff -rq` over the boundary set reports only
      files whose divergence is listed in
      [tech-docs §2.8.1](./tech-docs.md#281-audit-result), and **zero** unlisted differences. Any
      unlisted difference is an unmigrated capability: stop, upstream it into `ose-public` first, and
      re-run. This step is the guard against silently deleting work.
- [ ] [AI] Confirm every upstreamed capability is present in canonical **before** the copy —
      commands: `cargo test --manifest-path /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/Cargo.toml --lib docs::naming`,
      `cargo test --manifest-path /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/Cargo.toml scan_fsharp`, and
      `cargo test --manifest-path /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/Cargo.toml --test cargo_target_share`
      — acceptance: all exit 0 and `project.json` clears all three inherited Git variables.
- [ ] [AI] Copy canonical `apps/rhino-cli` — command:
      `rsync -a --delete /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/apps/rhino-cli/ /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/apps/rhino-cli/` — acceptance: `diff -r`
      reports no difference across the boundary set, and `... -- parity manifest validate` exits 0
      without regenerating.
- [ ] [AI] Confirm `md naming validate` still passes on this repo's own `ROADMAP.md` and
      `SECURITY.md` after the copy — acceptance: the command exits 0. This is the falsifiable proof
      that the copy preserved the capability rather than reverting it.
- [ ] [AI] **P5-REGISTRY-AUTHORING** — Author `beaver-nest`'s `gates:` section from
      [`repo-configs/repo-config-beaver-nest.yml`](./repo-configs/repo-config-beaver-nest.yml),
      which prunes the **nine** formatter entries this repo declares for languages it does not track
      (Go, Elixir, C#, Clojure, Dart, Lua, C, Bazel, Terraform) plus the `*.sql` prettier glob, which
      matches zero tracked files here — acceptance:
      `... -- repo-config validate` exits 0, and
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 5'`
      exits 0 (prettier, rustfmt, shfmt, fantomas, ruff — the five languages it actually tracks).
- [ ] [AI] **P5-CONFIG-COPY** (`blockedBy: P5-REGISTRY-AUTHORING`; `blocks: P5-PACKAGE-COPY`) —
      install the authored registry without its audit banner — command:
      `sed -n '/^# repo-config.yml — schema:/,$p' /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/repo-configs/repo-config-beaver-nest.yml > /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/repo-config.yml`
      — acceptance: `(cd /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement && npm exec nx -- run rhino-cli:repo-config-validation)` exits 0.
- [ ] [AI] **P5-PACKAGE-COPY** (`blockedBy: P5-CONFIG-COPY`; `blocks: P5-HOOK-COMMIT-MSG`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/package-json/package-beaver-nest.json /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/package.json`
      — acceptance: `jq empty /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/package.json` exits 0.
- [ ] [AI] **P5-HOOK-COMMIT-MSG** (`blockedBy: P5-PACKAGE-COPY`; `blocks: P5-HOOK-PRE-COMMIT`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/commit-msg-beaver-nest.sh /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/commit-msg`
      — acceptance: `sh -n /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/commit-msg` exits 0.
- [ ] [AI] **P5-HOOK-PRE-COMMIT** (`blockedBy: P5-HOOK-COMMIT-MSG`; `blocks: P5-HOOK-PRE-PUSH`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-commit-beaver-nest.sh /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/pre-commit`
      — acceptance: `sh -n /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/pre-commit` exits 0.
- [ ] [AI] **P5-HOOK-PRE-PUSH** (`blockedBy: P5-HOOK-PRE-COMMIT`; `blocks: P5-PR-WORKFLOW`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/plans/in-progress/sdlc-gate-registry-enforcement/husky-hooks/pre-push-beaver-nest.sh /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/pre-push`
      — acceptance: `sh -n /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.husky/pre-push` exits 0.
- [ ] [AI] **P5-PR-WORKFLOW** (`blockedBy: P5-HOOK-PRE-PUSH`; `blocks: P5-DEPS-COPY`) — replace
      the hand-written gate list in the exact destination
      `/Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/pr-quality-gate.yml`
      with enumerate/matrix jobs while preserving Beaver's toolchain setup and `name: Quality gate`
      join job — acceptance: `actionlint /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/pr-quality-gate.yml` exits 0.
- [ ] [AI] **P5-DEPS-COPY** (`blockedBy: P5-PR-WORKFLOW`; `blocks: P5-DEPS-DELETE`) — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/.github/workflows/dependency-vulnerability-audit.yml /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/dependency-vulnerability-audit.yml`
      — acceptance: `actionlint /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/dependency-vulnerability-audit.yml` exits 0.
- [ ] [AI] **P5-DEPS-DELETE** (`blockedBy: P5-DEPS-COPY`; `blocks: P5-PARITY-WORKFLOW`) — command:
      `git -C /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement rm .github/workflows/deps-audit.yml`
      — acceptance: `test ! -f /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/deps-audit.yml` exits 0.
- [ ] [AI] **P5-PARITY-WORKFLOW** (`blockedBy: P5-DEPS-DELETE`; `blocks: P5-MAIN-CI-DELETE`) —
      command: `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/.github/workflows/rhino-cli-parity-audit.yml /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/rhino-cli-parity-audit.yml`
      — acceptance: `actionlint /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/rhino-cli-parity-audit.yml` exits 0.
- [ ] [AI] **P5-MAIN-CI-DELETE** (`blockedBy: P5-PARITY-WORKFLOW`; `blocks: P5-DOCS`) — command:
      `git -C /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement rm .github/workflows/main-ci.yml`
      — acceptance: `test ! -f /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/.github/workflows/main-ci.yml` exits 0.
- [ ] [AI] Copy finalized standard — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/docs/reference/sdlc-gate-standard.md /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/docs/reference/sdlc-gate-standard.md`
      — acceptance: destination exists.
- [ ] [AI] Copy rewritten hook lifecycle — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/repo-governance/development/workflow/git-hook-lifecycle.md /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/repo-governance/development/workflow/git-hook-lifecycle.md`
      — acceptance: destination exists.
- [ ] [AI] **P5-PROPAGATION** — Copy fork-removal related-repositories amendment — command:
      `cp /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-rewire-public/docs/reference/related-repositories.md /Users/wkf/ose-projects/beaver-nest/worktrees/sdlc-gate-registry-enforcement/docs/reference/related-repositories.md`
      — acceptance: `npm run lint:md` exits 0 and no in-progress plan folder is added to `beaver-nest`.

### Phase 5 Execution-Ready Gate

- [ ] [AI] **P5-READY** (`blockedBy: P5-PROPAGATION`; `blocks: P5-LAND`) — commands:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` and
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: both exit
      0 before any Phase 5 Land action begins.

Every non-merge Land checkbox below is `blockedBy: P5-READY`; the untagged protected merge checkbox
remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit Phase 5 — command: `git add -- apps/rhino-cli .husky .github package.json repo-config.yml AGENTS.md docs repo-governance && git commit -m 'feat(ci): converge beaver-nest registry gates'` — acceptance: commitlint and sync validation exit 0.
- [ ] [AI] Push Phase 5 — command: `git push -u origin sdlc-gate-registry-enforcement` — acceptance: exits 0.
- [ ] [AI] Open draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement --fill` — acceptance: one PR exists.
- [ ] [AI] Cycle 1 makers — invoke eight makers — acceptance: eight reports.
- [ ] [AI] Cycle 1 synthesis — invoke synthesis maker — acceptance: one posted review.
- [ ] [AI] Cycle 1 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 1 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix, commit, push before Cycle 2.
- [ ] [AI] Cycle 2 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 2 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 2 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 2 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before Cycle 3.
- [ ] [AI] Cycle 3 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 3 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 3 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 3 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft false and five preconditions pass.
- [ ] [AI] Merge.
- [ ] [AI] Fetch `origin/main`, prove the old local `main` is an ancestor, then atomically
      fast-forward the bare repo's local ref without removing any worktree —
      commands:
      `git -C /Users/wkf/ose-projects/beaver-nest fetch origin main`,
      `git -C /Users/wkf/ose-projects/beaver-nest merge-base --is-ancestor main origin/main`, and
      `git -C /Users/wkf/ose-projects/beaver-nest update-ref refs/heads/main refs/remotes/origin/main refs/heads/main`
      — acceptance: every command exits 0,
      `git -C /Users/wkf/ose-projects/beaver-nest rev-list --left-right --count main...origin/main` reports
      `0 0`; the delivery worktree remains available until terminal prompted cleanup, and unrelated
      worktrees remain untouched.

### Phase 5 Gate

> All checks below must pass before starting Phase 6 (Phase 5 is blocked by Phase 2, independent of
> Phases 3 and 4, and one of three nodes that block Phase 6).

- [ ] [AI] `... -- gate validate` exits 0 in `beaver-nest`.
- [ ] [AI] `apps/rhino-cli` byte-identical to `ose-public`'s Phase 11 result — acceptance: `diff -r`
      over the boundary set reports zero differences.
- [ ] [AI] `... -- parity manifest validate` exits 0.
- [ ] [AI] `md naming validate` passes on this repo's `ROADMAP.md` and `SECURITY.md`.
- [ ] [AI] The F# environment-wrapper and framework-owned-key regressions pass in the converged
      source — commands: `cargo test --manifest-path apps/rhino-cli/Cargo.toml scan_fsharp` and
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test env` — acceptance: both exit 0.
- [ ] [AI] Rust test targets still isolate inherited Git process state — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test cargo_target_share` — acceptance:
      exits 0 and the three target commands clear all three Git variables.
- [ ] [AI] No document in any repo still calls `beaver-nest` a fork of `rhino-cli` — acceptance:
      `/usr/bin/grep -rln "beaver-nest.*fork" docs/ repo-governance/ AGENTS.md` returns no match.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git -C /Users/wkf/ose-projects/beaver-nest rev-list --left-right --count main...origin/main`
      — acceptance: reports `0 0`.

> **Pause Safety**: `beaver-nest`'s hooks and CI derive from the registry; it is no longer documented
> as a fork; `apps/rhino-cli` matches canonical; the merge is on `main`; the task-owned worktree is
> retained. Safe to stop. To resume: run `... -- gate validate` in that worktree, then start Phase 6
> once Phases 3 and 4 also merge.

---

## Phase 6 — Knowledge Capture (`ose-public`, PR #6)

Terminal node. Blocked by Phases 2, 3, 4, and 5.

- [ ] [AI] Create the Phase 6 `ose-public` worktree from converged `origin/main` — commands:
      `git fetch origin main` and
      `git worktree add -b sdlc-gate-registry-enforcement-knowledge worktrees/sdlc-gate-registry-enforcement-knowledge origin/main`
      — acceptance: the worktree is clean and `HEAD...origin/main` reports `0 0`.
- [ ] [AI] Install its dependencies — command:
      `npm --prefix worktrees/sdlc-gate-registry-enforcement-knowledge install` — acceptance: exits 0.
- [ ] [AI] Initialize its toolchain — command:
      `(cd worktrees/sdlc-gate-registry-enforcement-knowledge && npm run doctor -- --fix)` —
      acceptance: exits 0 and a subsequent doctor check reports no missing tool.
- [ ] [AI] Attach a detached final-verification worktree to `beaver-nest`'s converged `origin/main` —
      commands: `git -C /Users/wkf/ose-projects/beaver-nest fetch origin main` and
      `git -C /Users/wkf/ose-projects/beaver-nest worktree add --detach worktrees/gate-final-verification origin/main`
      — acceptance: it is clean at the exact `origin/main` SHA and unrelated worktrees are unchanged.
- [ ] [AI] Install and initialize the final-verification worktree — commands:
      `npm --prefix /Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification install` and
      `(cd /Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification && npm run doctor -- --fix)` —
      acceptance: both exit 0 and a subsequent doctor check reports no missing tool.

### 6.1 Verification

- [ ] [AI] **P6-END-STATE** (`blocks: P6-COMPOSITION-SETUP`) — validate four exact working roots and
      prove each is level with its converged `origin/main` — commands:

  ```bash
  for P6_ROOT in \
    /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge \
    /Users/wkf/ose-projects/ose-primer \
    /Users/wkf/ose-projects/ose-private \
    /Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  do
    test -d "$P6_ROOT"
    git -C "$P6_ROOT" fetch origin main
    test "$(git -C "$P6_ROOT" rev-list --left-right --count HEAD...origin/main)" = "0 0"
    (cd "$P6_ROOT" && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate)
    test ! -f "$P6_ROOT/.github/workflows/main-ci.yml"
  done
  ```

  Acceptance: every command exits 0 in all four roots.

- [ ] [AI] **P6-COMPOSITION-SETUP** (`blockedBy: P6-END-STATE`; `blocks: P6-COMPOSITION-ASSERT`) —
      create one exact scratch composition violation only after proving the target is clean — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge
  git -C "$P6_ROOT" diff --quiet -- repo-config.yml
  printf '%s\n' \
    '  - id: p6-composition-inverse' \
    '    type: check' \
    '    command: repo-config validate' \
    '    kind: rhino-cli' \
    '    surfaces:' \
    '      pre-commit: { scope: other }' >> "$P6_ROOT/repo-config.yml"
  rg -n 'id: p6-composition-inverse' "$P6_ROOT/repo-config.yml"
  ```

  Acceptance: the final command prints exactly one scratch gate.

- [ ] [AI] **P6-COMPOSITION-ASSERT** (`blockedBy: P6-COMPOSITION-SETUP`; `blocks: P6-COMPOSITION-CLEANUP`) —
      prove the validator rejects the scratch gate — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge
  P6_LOG="$P6_ROOT/local-temp/p6-composition-inverse.log"
  if (cd "$P6_ROOT" && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate > "$P6_LOG" 2>&1)
  then
    exit 1
  fi
  rg -n 'p6-composition-inverse|Gate Composition Rule|missing.*ci' "$P6_LOG"
  ```

  Acceptance: validation is non-zero and the log names the scratch gate or missing CI composition.

- [ ] [AI] **P6-COMPOSITION-CLEANUP** (`blockedBy: P6-COMPOSITION-ASSERT`; `blocks: P6-BYTE-IDENTITY`) —
      restore only the scratch target and revalidate the clean state — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge
  git -C "$P6_ROOT" restore -- repo-config.yml
  rm -f "$P6_ROOT/local-temp/p6-composition-inverse.log"
  git -C "$P6_ROOT" diff --quiet -- repo-config.yml
  (cd "$P6_ROOT" && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate)
  ```

  Acceptance: the restored file is clean and validation exits 0.

- [ ] [AI] **P6-BYTE-IDENTITY** (`blockedBy: P6-COMPOSITION-CLEANUP`; `blocks: P6-PARITY-SETUP`) —
      compare every boundary path directly from canonical to each downstream root — commands:

  ```bash
  P6_CANONICAL=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge
  for P6_DOWNSTREAM in \
    /Users/wkf/ose-projects/ose-primer \
    /Users/wkf/ose-projects/ose-private \
    /Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  do
    for P6_PATH in \
      apps/rhino-cli/src \
      apps/rhino-cli/tests \
      apps/rhino-cli/Cargo.toml \
      apps/rhino-cli/Cargo.lock \
      apps/rhino-cli/project.json \
      apps/rhino-cli/LICENSE \
      apps/rhino-cli/parity-manifest.sha256 \
      specs/apps/rhino/behavior/rhino-cli/gherkin
    do
      diff -r "$P6_CANONICAL/$P6_PATH" "$P6_DOWNSTREAM/$P6_PATH"
    done
  done
  ```

  Acceptance: every pairwise `diff -r` exits 0.

- [ ] [AI] **P6-PARITY-SETUP** (`blockedBy: P6-BYTE-IDENTITY`; `blocks: P6-PARITY-ASSERT`) — create
      one real drift in the clean detached Beaver verification worktree — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  git -C "$P6_ROOT" diff --quiet -- apps/rhino-cli/LICENSE
  printf '%s\n' '# p6 parity inverse scratch' >> "$P6_ROOT/apps/rhino-cli/LICENSE"
  git -C "$P6_ROOT" diff --quiet -- apps/rhino-cli/LICENSE && exit 1 || true
  ```

  Acceptance: only `apps/rhino-cli/LICENSE` is dirty.

- [ ] [AI] **P6-PARITY-ASSERT** (`blockedBy: P6-PARITY-SETUP`; `blocks: P6-PARITY-CLEANUP`) — prove
      manifest validation fails and names the drifted file — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  P6_LOG="$P6_ROOT/local-temp/p6-parity-inverse.log"
  if (cd "$P6_ROOT" && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate > "$P6_LOG" 2>&1)
  then
    exit 1
  fi
  rg -n 'LICENSE' "$P6_LOG"
  ```

  Acceptance: validation is non-zero and the log names `LICENSE`.

- [ ] [AI] **P6-PARITY-CLEANUP** (`blockedBy: P6-PARITY-ASSERT`; `blocks: P6-AUDIT-DISPATCH`) — restore
      only the scratch file and prove parity is green again — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  git -C "$P6_ROOT" restore -- apps/rhino-cli/LICENSE
  rm -f "$P6_ROOT/local-temp/p6-parity-inverse.log"
  git -C "$P6_ROOT" diff --quiet -- apps/rhino-cli/LICENSE
  (cd "$P6_ROOT" && cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- parity manifest validate)
  ```

  Acceptance: the file is clean and validation exits 0.

- [ ] [AI] **P6-AUDIT-DISPATCH** (`blockedBy: P6-PARITY-CLEANUP`; `blocks: P6-AUDIT-ASSERT`) — dispatch
      the exact converged workflow in all four repositories — commands:

  ```bash
  for P6_REPO in \
    wahidyankf/ose-public \
    wahidyankf/ose-primer \
    wahidyankf/ose-private \
    wahidyankf/beaver-nest
  do
    gh workflow run rhino-cli-parity-audit.yml --repo "$P6_REPO" --ref main
  done
  ```

  Acceptance: all four dispatch commands exit 0.

- [ ] [AI] **P6-AUDIT-ASSERT** (`blockedBy: P6-AUDIT-DISPATCH`; `blocks: P6-AUDIT-INVERSE-SETUP`) —
      after each two-minute scheduled wakeup, identify the exact newest manual run and inspect it —
      commands:

  ```bash
  for P6_REPO in \
    wahidyankf/ose-public \
    wahidyankf/ose-primer \
    wahidyankf/ose-private \
    wahidyankf/beaver-nest
  do
    P6_RUN_ID=$(gh run list --repo "$P6_REPO" --workflow rhino-cli-parity-audit.yml --branch main --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId')
    test -n "$P6_RUN_ID"
    gh run view "$P6_RUN_ID" --repo "$P6_REPO" --json status,conclusion --jq '.status == "completed" and .conclusion == "success"' | grep -Fx true
  done
  ```

  Acceptance: repeat only this inspection at the prescribed interval until all four print `true`;
  fix every real failure before continuing.

- [ ] [AI] **P6-AUDIT-INVERSE-SETUP** (`blockedBy: P6-AUDIT-ASSERT`; `blocks: P6-AUDIT-INVERSE-DISPATCH`) —
      create and push one task-owned scratch branch with a deliberately divergent manifest — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  P6_BRANCH=p6-parity-audit-inverse
  if git -C "$P6_ROOT" ls-remote --exit-code --heads origin "$P6_BRANCH" >/dev/null 2>&1
  then
    exit 1
  fi
  git -C "$P6_ROOT" switch -c "$P6_BRANCH" origin/main
  printf '%s\n' 'p6 deliberate invalid manifest row' >> "$P6_ROOT/apps/rhino-cli/parity-manifest.sha256"
  git -C "$P6_ROOT" add -- apps/rhino-cli/parity-manifest.sha256
  git -C "$P6_ROOT" commit -m 'test(ci): verify parity audit rejects drift'
  git -C "$P6_ROOT" push -u origin "$P6_BRANCH"
  ```

  Acceptance: the exact scratch branch exists on origin with one manifest-only commit.

- [ ] [AI] **P6-AUDIT-INVERSE-DISPATCH** (`blockedBy: P6-AUDIT-INVERSE-SETUP`; `blocks: P6-AUDIT-INVERSE-ASSERT`) —
      dispatch the audit against the exact scratch ref — command:
      `gh workflow run rhino-cli-parity-audit.yml --repo wahidyankf/beaver-nest --ref p6-parity-audit-inverse`
      — acceptance: exits 0.

- [ ] [AI] **P6-AUDIT-INVERSE-ASSERT** (`blockedBy: P6-AUDIT-INVERSE-DISPATCH`; `blocks: P6-AUDIT-INVERSE-CLEANUP`) —
      after each two-minute scheduled wakeup, identify and inspect the exact scratch run — commands:

  ```bash
  P6_RUN_ID=$(gh run list --repo wahidyankf/beaver-nest --workflow rhino-cli-parity-audit.yml --branch p6-parity-audit-inverse --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId')
  test -n "$P6_RUN_ID"
  gh run view "$P6_RUN_ID" --repo wahidyankf/beaver-nest --json status,conclusion --jq '.status == "completed" and .conclusion == "failure"' | grep -Fx true
  ```

  Acceptance: repeat only this inspection at the prescribed interval until it prints `true`.

- [ ] [AI] **P6-AUDIT-INVERSE-CLEANUP** (`blockedBy: P6-AUDIT-INVERSE-ASSERT`; `blocks: P6-FORMATTER-PRESENCE`) —
      remove only the task-owned scratch refs and return the worktree to clean detached main — commands:

  ```bash
  P6_ROOT=/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification
  P6_BRANCH=p6-parity-audit-inverse
  git -C "$P6_ROOT" push origin --delete "$P6_BRANCH"
  git -C "$P6_ROOT" switch --detach origin/main
  git -C "$P6_ROOT" branch -D "$P6_BRANCH"
  test -z "$(git -C "$P6_ROOT" status --porcelain)"
  ```

  Acceptance: local and remote scratch refs are absent and the detached worktree is clean.

- [ ] [AI] **P6-FORMATTER-PRESENCE** (`blockedBy: P6-AUDIT-INVERSE-CLEANUP`; `blocks: P6-PROTECTION-ASSERT`) —
      mechanically expand every formatter glob and require at least one tracked match — command:

  ```bash
  cd /Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge
  node - <<'NODE'
  const { execFileSync } = require('node:child_process');
  const fs = require('node:fs');
  const braces = require('braces');
  const picomatch = require('picomatch');
  const YAML = require('yaml');
  const roots = [
    '/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge',
    '/Users/wkf/ose-projects/ose-primer',
    '/Users/wkf/ose-projects/ose-private',
    '/Users/wkf/ose-projects/beaver-nest/worktrees/gate-final-verification',
  ];
  for (const root of roots) {
    const files = execFileSync('git', ['-C', root, 'ls-files'], { encoding: 'utf8' }).trim().split('\n');
    const config = YAML.parse(fs.readFileSync(`${root}/repo-config.yml`, 'utf8'));
    for (const gate of config.gates.filter((entry) => entry.category === 'formatter')) {
      const patterns = Object.values(gate.surfaces)
        .flatMap((surface) => surface.globs || [surface.glob])
        .filter(Boolean);
      for (const pattern of patterns.flatMap((item) => braces.expand(item))) {
        if (!files.some(picomatch(pattern, { basename: true }))) {
          throw new Error(`${root}: ${gate.id} has no ${pattern}`);
        }
      }
    }
  }
  NODE
  ```

  Acceptance: Node exits 0 without a zero-match formatter extension.

- [ ] [AI] **P6-PROTECTION-ASSERT** (`blockedBy: P6-FORMATTER-PRESENCE`; `blocks: P6-PROTECTION-CLEANUP`) —
      run four separate valid endpoints and assert the Phase 0 observations — commands:

  ```bash
  P6_TMP=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge/local-temp
  mkdir -p "$P6_TMP"
  gh api repos/wahidyankf/ose-public/branches/main/protection | jq -e '.required_status_checks.contexts == ["Quality gate"]'
  for P6_EXPECTATION in ose-primer:404 ose-private:403 beaver-nest:404
  do
    P6_REPO=${P6_EXPECTATION%%:*}
    P6_STATUS=${P6_EXPECTATION##*:}
    P6_LOG="$P6_TMP/p6-protection-$P6_REPO.log"
    if gh api "repos/wahidyankf/$P6_REPO/branches/main/protection" > "$P6_LOG" 2>&1
    then
      exit 1
    fi
    rg -n "HTTP $P6_STATUS" "$P6_LOG"
  done
  ```

  Acceptance: public prints `true`; primer/private/Beaver logs explicitly print 404/403/404.

- [ ] [AI] **P6-PROTECTION-CLEANUP** (`blockedBy: P6-PROTECTION-ASSERT`) — remove only the three
      task-owned API logs — commands:

  ```bash
  P6_TMP=/Users/wkf/ose-projects/ose-public/worktrees/sdlc-gate-registry-enforcement-knowledge/local-temp
  rm -f \
    "$P6_TMP/p6-protection-ose-primer.log" \
    "$P6_TMP/p6-protection-ose-private.log" \
    "$P6_TMP/p6-protection-beaver-nest.log"
  test ! -e "$P6_TMP/p6-protection-ose-primer.log"
  test ! -e "$P6_TMP/p6-protection-ose-private.log"
  test ! -e "$P6_TMP/p6-protection-beaver-nest.log"
  ```

  Acceptance: all three scratch logs are absent.

- [ ] [HUMAN] **Only if P6-PROTECTION-ASSERT fails**: update the required-status-check contexts in
      repository settings. Human-gated because it is a settings change outside the git tree, it is
      not covered by any PR review, and a wrong value silently unblocks every future merge. If the
      assertion passes, strike this step as not-applicable rather than performing it. Observable
      resume signal: P6-PROTECTION-ASSERT passes when rerun with the exact commands above.

### 6.2 Knowledge Capture

- [ ] [AI] Apply the litmus test to every [learnings.md](./learnings.md) entry — keep only entries
      where a durable surface would catch this automatically next time; discard the rest with a
      one-line reason.
- [ ] [AI] Apply the secret/sensitivity gate to every surviving entry — sanitize to `{placeholder}`
      tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the repo-relevance gate to every surviving entry — content sourced from
      `ose-private` stays in `ose-private` only; never cross-route it into `ose-public`, `ose-primer`,
      or `beaver-nest`. This gate is load-bearing here, since `ose-private` is one of the four repos
      in scope.
- [ ] [AI] Route each surviving entry to exactly one durable home (`docs/`, `repo-governance/`,
      `.claude/agents/`, `.claude/skills/`, or another durable home), landing small non-code edits
      inline or filing a `plans/backlog/{slug}/` follow-up plan for larger non-code work.
- [ ] [AI] Code-routing rule: if a learning's home is `apps/`, `libs/`, or tests, file it as a
      separate `plans/backlog/` plan — never land it inline in this PR's commits. The sole carve-out
      is a bug/lint/test failure blocking this plan's own scope, fixed inline as ordinary Root Cause
      Orientation work.
- [ ] [AI] Record the terminal state of every entry (routed inline / filed as backlog at `{path}` /
      discarded with reason) directly in `learnings.md`, or record the explicit
      `No generalizable learnings — {reason}` escape — acceptance: no untriaged entry remains.

### 6.3 Archive the Plan (`ose-public`)

- [ ] [AI] Archive the plan in `ose-public` — command:
      `ARCHIVE_DATE=$(date +%F) && git mv plans/in-progress/sdlc-gate-registry-enforcement/ "plans/done/${ARCHIVE_DATE}__sdlc-gate-registry-enforcement/"`
      — acceptance: the folder exists under `done/` with today's validated date prefix,
      and `plans/in-progress/README.md` no longer lists it.
- [ ] [AI] Update `plans/done/README.md` and `plans/in-progress/README.md` in `ose-public` —
      acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done`
      exits 0.
- [ ] [AI] **P6-ARCHIVE** — Retire `plans/ideas/tri-repo-rhino-cli-byte-identity-gate.md`: this plan's R-11/R-12
      fulfill it — delete the file — acceptance: `test -f plans/ideas/tri-repo-rhino-cli-byte-identity-gate.md`
      exits non-zero, and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done`
      still exits 0 (no remaining reference to the deleted file).

### Phase 6 Execution-Ready Gate

- [ ] [AI] **P6-READY** (`blockedBy: P6-ARCHIVE`; `blocks: P6-LAND`) — verify §6.1–§6.3,
      including the already-staged archival, then run
      `npm exec nx -- affected -t typecheck,lint,test:quick,specs:coverage` — acceptance: every
      specified verification exits as expected, the dated plan folder is under `plans/done/`, and
      the Nx command exits 0 before any Phase 6 Land action begins.

### 6.4 Land

Every non-merge checkbox in this subsection is `blockedBy: P6-READY`; the untagged protected merge
checkbox remains the separately authorized integration action after its preceding Land tasks.

- [ ] [AI] Commit Phase 6 — command: `git add -- plans repo-governance && git commit -m 'docs(plans): archive gate registry delivery knowledge'` — acceptance: commitlint and sync validation exit 0.
- [ ] [AI] Push Phase 6 — command: `git push -u origin sdlc-gate-registry-enforcement-knowledge` — acceptance: exits 0 and matches the declared branch.
- [ ] [AI] Open draft PR — command: `gh pr create --draft --base main --head sdlc-gate-registry-enforcement-knowledge --fill` — acceptance: one PR exists.
- [ ] [AI] Cycle 1 makers — invoke eight makers — acceptance: eight reports.
- [ ] [AI] Cycle 1 synthesis — invoke synthesis maker — acceptance: one posted review.
- [ ] [AI] Cycle 1 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 1 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-knowledge --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; fix, commit, push before Cycle 2.
- [ ] [AI] Cycle 2 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 2 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 2 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 2 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-knowledge --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before Cycle 3.
- [ ] [AI] Cycle 3 makers — invoke eight makers — acceptance: eight fresh reports.
- [ ] [AI] Cycle 3 synthesis — invoke synthesis maker — acceptance: fresh review.
- [ ] [AI] Cycle 3 fixer — invoke fixer — acceptance: fixes committed/pushed.
- [ ] [AI] Cycle 3 CI — command: `RUN_ID=$(gh run list --branch sdlc-gate-registry-enforcement-knowledge --workflow pr-quality-gate.yml --limit 1 --json databaseId --jq '.[0].databaseId') && gh run view "$RUN_ID" --json status,conclusion` — acceptance: completed/success; repair before readiness.
- [ ] [AI] Mark ready — command: `gh pr ready` — acceptance: draft false and five preconditions pass.
- [ ] [AI] Merge PR #6.
- [ ] [AI] Fast-forward local `main` after the merge — command:
      `git fetch origin main && git switch main && git merge --ff-only origin/main` — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### 6.5 Prompted Cleanup — Terminal DAG Node

No sibling repo receives an in-progress copy of this plan in Phases 3, 4, or 5, so sibling archival
is not applicable. The authoritative plan is archived in `ose-public` inside PR #6.

- [ ] [AI] Inventory only the task-owned worktree paths declared in this plan, including
      `beaver-nest/worktrees/gate-final-verification`; inspect `git status --porcelain`, unpushed
      commits, and each dirty diff — acceptance: every task-owned worktree is clean and fully pushed,
      or its evidence is recovered before cleanup. Unrelated worktrees are recorded and excluded.
- [ ] [HUMAN] Confirm removal of the inventoried task-owned worktrees and their local delivery
      branches — acceptance: explicit confirmation is recorded; without it, leave every worktree in
      place and mark cleanup pending rather than deleting anything.
- [ ] [AI] **CLEAN-PUBLIC-1** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-public worktree remove worktrees/sdlc-gate-registry-enforcement` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PUBLIC-1B** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-public worktree remove worktrees/sdlc-gate-registry-enforcement-defork` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PUBLIC-2** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-public worktree remove worktrees/sdlc-gate-registry-enforcement-rewire-public` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PUBLIC-6** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-public worktree remove worktrees/sdlc-gate-registry-enforcement-knowledge` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PRIMER** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-primer worktree remove worktrees/sdlc-gate-registry-enforcement` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PRIVATE** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/ose-private worktree remove worktrees/sdlc-gate-registry-enforcement` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-BEAVER-DELIVERY** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/beaver-nest worktree remove worktrees/sdlc-gate-registry-enforcement` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-BEAVER-VERIFY** (`blockedBy: HUMAN-CLEANUP-CONFIRM`) — command: `git -C /Users/wkf/ose-projects/beaver-nest worktree remove worktrees/gate-final-verification` — acceptance: exits 0; unrelated worktrees remain.
- [ ] [AI] **CLEAN-PRUNE** (`blockedBy: CLEAN-PUBLIC-1, CLEAN-PUBLIC-1B, CLEAN-PUBLIC-2, CLEAN-PUBLIC-6, CLEAN-PRIMER, CLEAN-PRIVATE, CLEAN-BEAVER-DELIVERY, CLEAN-BEAVER-VERIFY`) — command: `git -C /Users/wkf/ose-projects/ose-public worktree prune && git -C /Users/wkf/ose-projects/ose-primer worktree prune && git -C /Users/wkf/ose-projects/ose-private worktree prune && git -C /Users/wkf/ose-projects/beaver-nest worktree prune` — acceptance: task-owned paths are absent from all four inventories; unrelated worktrees remain.

### Phase 6 Gate

> These checks verify the integrated archival and terminal cleanup state after authorized Land.

- [ ] [AI] All four repos verified (§6.1) — acceptance: every command in §6.1 exits as specified.
- [ ] [AI] `learnings.md` fully triaged (§6.2) — acceptance: every entry is terminal, or the explicit
      "none" escape is recorded.
- [ ] [AI] Confirm the landed ref matches `origin/main` — command:
      `git rev-list --left-right --count HEAD...origin/main` — acceptance: reports `0 0`.
- [ ] [AI] Authoritative plan archived in `ose-public` (§6.3); no sibling in-progress plan copy exists
      — acceptance: the dated folder exists under `ose-public/plans/done/`, the public in-progress
      index no longer lists it, and the sibling repos contain no tracked
      `plans/in-progress/sdlc-gate-registry-enforcement/` folder.
- [ ] [AI] Prompted cleanup resolved (§6.5) — acceptance: after confirmation, all task-owned paths
      are absent and all unrelated worktrees remain; without confirmation, cleanup is explicitly
      pending and no deletion occurred.

> **Pause Safety**: Before integration, the archival branch is execution-ready and safe to stop.
> After authorized integration, all four mains are green and the authoritative plan is archived.
> Resume by re-running this gate; cleanup removes only explicitly confirmed task-owned worktrees.

---

## Strict Plan-Checker Remediation

These tasks were added from the 2026-08-04 strict pre-execution report
`plan__1c0563__2026-08-04--14-24__audit.md`. They block all remaining Phase 0 work and every
change-producing phase until the report is clean.

- [x] [AI] **R10-PUBLIC-WORKTREE** — amend Phase 0 to use a declared attached `ose-public`
      worktree for every public working-tree command, and preserve the bare root for ref-only
      operations — acceptance: no Phase 0 public command invokes `git status` in the bare root.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md`
  - Notes: Declared the existing attached public worktree as Phase 0's public root, reopened its initialization tasks with worktree-scoped commands, and made the baseline cleanliness check exclude only plan-owned execution evidence.

- [x] [AI] **R10-P1-STAGING** — include the required Rhino Gherkin directory in the Phase 1 Land
      staging command — acceptance: the staged-diff assertion names both `apps/rhino-cli` and the
      Phase 1 Gherkin tree.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md`
  - Notes: Phase 1 Land now stages the bounded Gherkin tree and asserts that both the engine and Gherkin have staged paths before committing.

- [x] [AI] **R10-P1B-STAGING** — include `repo-config.yml` in the Phase 11 Land staging command
      and its staged-diff assertion — acceptance: the paired source/configuration change is
      mechanically required before the PR opens.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md`
  - Notes: Phase 11 Land now stages `repo-config.yml` and mechanically asserts it is paired with the shared-source change.

- [x] [AI] **R10-CANONICAL-SOURCE** — define one clean, merged, attached canonical `ose-public`
      source worktree and replace downstream reads from the bare root — acceptance: Phases 3–5
      copy only from that path after it proves `HEAD...origin/main` is `0 0`.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `plans/in-progress/sdlc-gate-registry-enforcement/delivery.md`
  - Notes: All Phase 3–5 canonical file reads now target the merged Phase 2 rewire worktree; Phase 2's gate proves that exact source path clean and level before any downstream copy.

- [x] [AI] **R10-BOUNDARY-IDENTIFIERS** — make all PR-bearing phases mechanically distinct to the
      numeric boundary detector and use the detector's exact lowercase `yes` token — acceptance:
      declared and actual PR-bearing phase sets compare equal, including the de-fork phase.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`
  - Notes: Renamed the de-fork delivery phase from non-numeric Phase 1b to numeric Phase 11 across the plan and changed PR-bearing boundary table values to the detector's lowercase `yes` token.

- [x] [AI] **R10-CLEAN-CHECK** — run strict plan validation from a clean detached checker worktree
      at the candidate plan commit — acceptance: the report has zero findings and does not confuse
      in-progress execution evidence with the pre-execution freshness gate.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: none (validation only)
  - Notes: Detached checker worktree at `20f63cce6d049ab9c0fa82f9453dcd234a89454e` produced `plan__54b995__2026-08-04--14-53__audit.md` with zero findings.

- [x] [AI] **R10-P2-FORMATTER-WRAPPER** — declare `scripts/format-elixir.sh` in the File-Impact
      Analysis and stage it in Phase 2 Land — acceptance: the wrapper and its test are authorized
      and reach the Phase 2 PR together.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `tech-docs.md`, `delivery.md`
  - Notes: Added the exact formatter-wrapper path to the declared footprint and made Phase 2 Land assert it is staged.

- [x] [AI] **R10-P2-HARNESS-STAGING** — stage every Phase 2 `.claude/` source and generated
      `.opencode/`, `.cursor/`, and `.amazonq/` mirror path — acceptance: the Phase 2 commit carries
      the generated binding set and `npm run validate:sync` confirms no divergence.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `delivery.md`
  - Notes: P2-HN-3 now stages the bounded canonical source and generated mirror directories immediately after generation; Phase 2 Land stages the same bounded set again defensively.

- [x] [AI] **R10-CANONICAL-GATE-ORDER** — move the canonical-source assertion from the Phase 1
      Gate to the Phase 2 Gate after its worktree exists — acceptance: no phase gate requires a
      future phase's worktree.
  - Date: 2026-08-04
  - Status: complete
  - Files Changed: `delivery.md`
  - Notes: Moved the canonical-source prerequisite into the Phase 2 Gate, after the rewire worktree has been created and merged.

## Settled Decisions

No open decisions remain. The one item previously carried as decided-with-recommendation is now
settled:

**`deps:audit` placement — settled 2026-08-02.** Excluded from the registry entirely, not declared
under a `cron` surface as the first draft proposed. It keeps its schedule and moves to its own
descriptively-named workflow, `dependency-vulnerability-audit.yml`. The `cron` surface is removed
from the schema; the registry covers the four gate surfaces and only those. Rationale in
[brd.md §A Standing Rule This Plan Upholds](./brd.md#a-standing-rule-this-plan-upholds) and
[tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).
