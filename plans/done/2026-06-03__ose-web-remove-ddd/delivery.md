# Delivery — ose-web-remove-ddd

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/ose-web-remove-ddd/`

Provision before execution (run from repo root):

```bash
claude --worktree ose-web-remove-ddd
```

Then initialize the toolchain (run in the **root** worktree, per
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md)):

```bash
npm install && npm run doctor -- --fix
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Provision the worktree from repo root: `claude --worktree ose-web-remove-ddd`
    — acceptance: `worktrees/ose-web-remove-ddd/` exists and is a valid git worktree.
<!-- Date: 2026-06-03 | Status: done | Notes: git worktree add provisioned at HEAD 796c75f8a -->
- [x] [AI] Install dependencies in the root worktree: `npm install`
<!-- Date: 2026-06-03 | Status: done | Notes: exits 0, 1563 packages -->
- [x] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
<!-- Date: 2026-06-03 | Status: done | Notes: exits 0, 20/20 tools OK, no drift -->
- [x] [AI] Record the current `apps_with_ddd()` length for the relative edit.
<!-- Date: 2026-06-03 | Status: done | Notes: N=4 (allowlist.rs line 31: assert_eq!(v.len(), 4)) — Plan 1 already decremented from 5 to 4 -->
- [x] [AI] Establish the `ose-web` + `rhino-cli` baseline.
<!-- Date: 2026-06-03 | Status: done | Notes: ALL PASS — ose-web: 136 tests, 97.27% coverage; rhino-cli: 782 tests; spec-coverage PASS -->
- [x] [AI] Establish the `rhino-cli` cargo baseline.
<!-- Date: 2026-06-03 | Status: done | Notes: 782 passed, membership test PASS -->
- [x] [AI] Resolve all preexisting failures before proceeding.
<!-- Date: 2026-06-03 | Status: done | Notes: NONE FOUND — all targets clean -->

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] `npx nx run-many -t typecheck lint test:quick spec-coverage -p ose-web rhino-cli` baseline recorded and every preexisting failure resolved (zero unresolved).
<!-- Date: 2026-06-03 | Status: done | Notes: all PASS -->
- [x] [AI] `cargo test --manifest-path apps/rhino-cli/Cargo.toml` baseline green.
<!-- Date: 2026-06-03 | Status: done | Notes: 782 passed -->
- [x] [AI] The current `apps_with_ddd()` expected length N is recorded.
<!-- Date: 2026-06-03 | Status: done | Notes: N=4 -->

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet. Safe to stop indefinitely. To resume: re-run the two baseline commands and
> confirm they are still clean.

---

## Phase 1: Remove rhino-cli DDD allowlist entry (RED→GREEN)

> _Suggested executor: `swe-rust-dev`_

This phase is a natural RED→GREEN: removing the slice entry makes the `membership` test fail (RED);
decrementing the expected length makes it pass (GREEN).

- [x] [AI] **RED** — Remove `"ose-platform",` from slice; membership test FAILS (left:3 right:4).
<!-- Date: 2026-06-03 | Status: done | Notes: test failed as expected -->
- [x] [AI] **GREEN** — Decrement assert_eq!(v.len(), 4) → 3; membership test PASSES. grep ose-platform = nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: 4 cascade fixes also in specs_validate_*.rs (same as Plan 1 pattern) -->
- [x] [AI] **REFACTOR** — Remove ose-platform doc line; full cargo test PASS; grep src/ = zero.
<!-- Date: 2026-06-03 | Status: done | Notes: 782 passed, 0 failed -->
- [x] [AI] Rebuild rhino-cli: `npx nx build rhino-cli` exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: build cached, exits 0 -->

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `cargo test --manifest-path apps/rhino-cli/Cargo.toml` — all tests pass.
<!-- Date: 2026-06-03 | Status: done | Notes: 777 passed (--lib) -->
- [x] [AI] `grep -n "ose-platform" apps/rhino-cli/src/` — zero matches.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] `npx nx build rhino-cli` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Commit: 015962282 -->

> **Pause Safety**: `rhino-cli` no longer lists `ose-platform` as a DDD app, its tests are green,
> and it is rebuilt. `ose-web` still references the (still-present) DDD specs, so the tree is
> coherent. Safe to stop. To resume: re-run `cargo test --manifest-path apps/rhino-cli/Cargo.toml`.

---

## Phase 2: De-DDD the ose-web pre-push gate (RED→GREEN)

> _Suggested executor: `swe-typescript-dev`_

- [x] [AI] **RED** — Confirm DDD commands present in project.json — matches found.
<!-- Date: 2026-06-03 | Status: done | Notes: 2 commands + 2 inputs globs confirmed -->
- [x] [AI] **GREEN** — Remove 2 ddd commands + 2 inputs globs from project.json. grep = zero. JSON valid.
<!-- Date: 2026-06-03 | Status: done | Files: apps/ose-web/project.json | Commit: 4f5c231f9 -->
- [x] [AI] **REFACTOR** — jq validates test:quick target exits 0.
<!-- Date: 2026-06-03 | Status: done -->

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] grep ddd bc/ul in project.json — zero matches.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] jq shows reduced command count.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] typecheck exits 0.
<!-- Date: 2026-06-03 | Status: done -->

> **Pause Safety**: `project.json` no longer invokes the DDD validators and the JSON is valid. The
> `ddd/` spec directory still exists (deleted next phase), so nothing dangles. Safe to stop. To
> resume: re-run the grep guard above.

---

## Phase 3: Delete the DDD spec registry (RED→GREEN)

> _Suggested executor: `specs-fixer`_

- [x] [AI] **RED** — `test -d specs/apps/ose-platform/ddd && echo PRESENT` — PRESENT confirmed.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] **GREEN** — `git rm -r specs/apps/ose-platform/ddd` — 11 files deleted.
<!-- Date: 2026-06-03 | Status: done | Commit: ffdfe4bf1 -->
- [x] [AI] **REFACTOR** — spec tree intact; git grep ose-platform/ddd = zero (outside README).
<!-- Date: 2026-06-03 | Status: done -->

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `test -d specs/apps/ose-platform/ddd` — exits non-zero. Directory gone.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] git grep ose-platform/ddd outside README = zero matches.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] `npx nx run ose-web:spec-coverage` — exits 0.
<!-- Date: 2026-06-03 | Status: done -->

> **Pause Safety**: the DDD registry is gone, `project.json` no longer references it, and
> `spec-coverage` (behavior-only) still passes. The README still has DDD prose (fixed next).
> Safe to stop. To resume: re-run the `git grep` guard above.

---

## Phase 4: Delete the empty domain layers (RED→GREEN)

> _Suggested executor: `swe-typescript-dev`_

- [x] [AI] **RED** — find domain | wc -l = 7; grep -rL "export {};" = nothing (all stubs).
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] **GREEN** — git rm all 7 domain/ folders. find domain | wc -l = 0.
<!-- Date: 2026-06-03 | Status: done | Commit: 8f0194890 -->
- [x] [AI] **REFACTOR** — git grep contexts/\*/domain in src = zero. typecheck exits 0.
<!-- Date: 2026-06-03 | Status: done -->

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] find domain = 0. Prints 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] typecheck exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] test:quick exits 0 (136 tests, 97.27% coverage).
<!-- Date: 2026-06-03 | Status: done -->

> **Pause Safety**: all DDD scaffolding (specs, validators, domain stubs) is removed and `ose-web`
> typechecks and passes `test:quick`. Only the README prose remains DDD-framed. Safe to stop. To
> resume: re-run `npx nx run ose-web:test:quick`.

---

## Phase 5: Rewrite the ose-web README (RED→GREEN)

> _Suggested executor: `readme-fixer`_

Rewrite the Architecture, Project-Structure, Specs, and Bounded-Contexts sections of
`apps/ose-web/README.md` to describe hexagonal feature modules (three layers: `application`,
`infrastructure`, `presentation`) per
`repo-governance/development/pattern/hexagonal-architecture-web.md`. Remove the `DDD` Architecture
bullet, the "DDD bounded contexts" Project-Structure comment, the entire "Bounded Contexts" table,
the `ddd/bounded-contexts.yaml` and `ddd/ubiquitous-language/` Specs rows, and the "schema v2" and
"Per-BC" phrasing. Update the "test:quick" comment so it no longer says "DDD validators".

- [x] [AI] **RED** — grep DDD terms in README — matches found.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] **GREEN** — Rewrite README: removed DDD bullet, BC table, ddd/ spec rows, Per-BC/schema v2. Added hexagonal-architecture-web.md link + 3 layers. grep = zero.
<!-- Date: 2026-06-03 | Status: done | Commit: 7a8d87a2b -->
- [x] [AI] **REFACTOR** — lint:md:fix + format:md both exit 0.
<!-- Date: 2026-06-03 | Status: done -->

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] grep DDD/BC/schema in README = zero matches.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] grep hexagonal-architecture-web.md in README — at least one match.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] lint:md exits 0 for README.
<!-- Date: 2026-06-03 | Status: done -->

> **Pause Safety**: all five change groups are now applied and the README is accurate. The tree is
> fully coherent. Safe to stop. To resume: proceed to the Phase 6 quality gates.

---

## Phase 6: Quality Gates, Manual Verification, Commit, and Push

> _Suggested executor: `ci-fixer` for CI follow-ups_

### Local Quality Gates (Before Push)

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Commit preexisting fixes separately with appropriate conventional
> commit messages.

- [x] [AI] Run affected typecheck — exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Run affected linting — exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Run affected quick tests — exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Run affected spec coverage — exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] run-many ose-web + rhino-cli all green.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] nx build ose-web exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] cargo test all pass (777 passed).
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Fix ALL failures — none found.
<!-- Date: 2026-06-03 | Status: done -->

### Manual UI Verification (Playwright MCP)

- [x] [AI] Start dev server port 3100.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Navigate + snapshot landing page — renders.
<!-- Date: 2026-06-03 | Status: done | Notes: 2 preexisting dev-mode hydration warnings in SocialIcons (not caused by our changes, production build clean) -->
- [x] [AI] Navigate + snapshot /updates — renders.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Navigate + snapshot /about — renders.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Console messages: /updates zero errors, /about zero errors; / has 2 preexisting dev-mode hydration warnings.
<!-- Date: 2026-06-03 | Status: done | Notes: preexisting hydration issue in SocialIcons component not caused by plan changes -->
- [x] [AI] Screenshots taken: local-temp/ose-landing-smoke.png, local-temp/ose-updates-smoke.png, local-temp/ose-about-smoke.png.
<!-- Date: 2026-06-03 | Status: done -->

### Commit Guidelines

- [x] [AI] Commits thematic: refactor(rhino-cli) 015962282, chore(ose-web) 4f5c231f9, chore(specs) ffdfe4bf1, refactor(ose-web) 8f0194890, docs(ose-web) 7a8d87a2b.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] No preexisting fixes needed separate commits.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] No bundled unrelated changes.
<!-- Date: 2026-06-03 | Status: done -->

### Post-Push CI Verification

- [x] [AI] Pushed to main.
<!-- Date: 2026-06-03 | Status: done | Notes: pushed at 49b7b5d58 -->
- [x] [AI] Monitored CI — triggered run 26857491265.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] ALL CI checks pass — run 26857491265 completed/success.
<!-- Date: 2026-06-03 | Status: done | Notes: all 7 jobs passed -->
- [x] [AI] No CI failures.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] CI green before archival.
<!-- Date: 2026-06-03 | Status: done -->

### Phase 6 Gate

> All checks below must pass before archival.

- [x] [AI] run-many ose-web + rhino-cli all green.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] nx build ose-web exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Playwright smoke: /updates + /about zero errors; / preexisting dev-mode warning only.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] CI run 26857491265 completed/success.
<!-- Date: 2026-06-03 | Status: done -->

---

## Plan Archival

- [x] [AI] Verify ALL delivery checklist items are ticked.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Verify ALL quality gates pass (local + CI).
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Verify ALL manual assertions pass (Playwright MCP smoke).
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Rename and move: git mv to plans/done/2026-06-03\_\_ose-web-remove-ddd.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Update plans/in-progress/README.md — ose-web-remove-ddd entry removed.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Update plans/done/README.md — entry added with completion date.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] No other READMEs reference this plan.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] Commit archival: chore(plans): move ose-web-remove-ddd to done.
<!-- Date: 2026-06-03 | Status: done -->
