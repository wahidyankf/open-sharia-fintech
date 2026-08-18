# Delivery Checklist — ayokoding-web Remove DDD

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.
>
> **Fix-all-issues**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root-cause-orientation principle — proactively fix preexisting errors
> encountered during work. Commit preexisting fixes separately with appropriate Conventional
> Commit messages.

## Worktree

Worktree path: `worktrees/ayokoding-web-remove-ddd/`

Provision before execution (run from repo root):

```bash
claude --worktree ayokoding-web-remove-ddd
```

Then initialize the toolchain **in the root worktree** (not the new worktree):

```bash
npm install && npm run doctor -- --fix
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md),
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md),
and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Provision the worktree from repo root: `claude --worktree ayokoding-web-remove-ddd`
    — acceptance: `worktrees/ayokoding-web-remove-ddd/` exists and is a valid git worktree
    (`git worktree list` shows it).
<!-- Date: 2026-06-03 | Status: done | Files Changed: worktrees/ayokoding-web-remove-ddd/ created via git worktree add | Notes: worktree provisioned at repo HEAD (ccc2574ea) -->
- [x] [AI] Install dependencies in the root worktree: `npm install`
    — acceptance: exits 0, `node_modules/` synchronized.
<!-- Date: 2026-06-03 | Status: done | Notes: npm install exited 0, 1563 packages, node_modules synced -->
- [x] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
    — acceptance: exits 0 with no unresolved drift (Rust/cargo, Node, Nx all present).
<!-- Date: 2026-06-03 | Status: done | Notes: doctor --fix exited 0, 20/20 tools OK, no drift -->
- [x] [AI] Establish the ayokoding-web + rhino-cli baseline:
    `npx nx run-many -t typecheck lint test:quick spec-coverage -p ayokoding-web rhino-cli`
    — acceptance: baseline pass/fail recorded; document every preexisting failure verbatim.
<!-- Date: 2026-06-03 | Status: done | Notes: ALL PASS — typecheck PASS, lint PASS (warnings non-blocking), test:quick PASS (341 tests, 86.21% coverage), spec-coverage PASS (75 scenarios, 236 steps), rhino-cli PASS (777 tests, 90% coverage) -->
- [x] [AI] Resolve all preexisting failures before proceeding (root-cause-orientation)
    — acceptance: no preexisting failures remain unresolved; if any are fixed, commit them
    separately (`fix(<scope>): ...`).
<!-- Date: 2026-06-03 | Status: done | Notes: NONE FOUND — all baseline targets passed, no preexisting failures -->
- [x] [AI] Confirm the current ground truth still matches `tech-docs.md`:
    `grep -n "ddd bc ayokoding\|ddd ul ayokoding" apps/ayokoding-web/project.json` and
    `grep -n "ayokoding" apps/rhino-cli/src/internal/allowlist.rs`
    — acceptance: the two `ddd` commands and the three `ayokoding` lines (doc, slice, assertion)
    are present; if not, STOP and reconcile the plan before editing.
<!-- Date: 2026-06-03 | Status: done | Notes: CONFIRMED — ddd bc/ul at lines 93-94, ayokoding in slice at line 24, assertion at line 40 -->

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
<!-- Date: 2026-06-03 | Status: done | Notes: both passed -->
- [x] [AI] `npx nx run-many -t typecheck lint test:quick spec-coverage -p ayokoding-web rhino-cli`
    baseline recorded and every preexisting failure resolved (zero unresolved).
<!-- Date: 2026-06-03 | Status: done | Notes: all targets PASS, zero preexisting failures -->

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no plan work
> exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx run-many -t typecheck lint test:quick spec-coverage -p ayokoding-web rhino-cli` and
> confirm it is still clean.

---

## Phase 1: Remove ayokoding from the rhino-cli DDD allowlist

> Natural RED→GREEN: adjust the `membership` test to its post-removal shape first (it fails
> against the current five-entry slice), then remove the slice entry to make it pass.
>
> _Suggested executor: `swe-rust-dev`_

- [x] [AI] **RED** — Edit the `membership` test in
    `apps/rhino-cli/src/internal/allowlist.rs`: read the current `assert_eq!(v.len(), N);`
    literal, decrement `N` by exactly one, and delete the line
    `assert!(v.contains(&"ayokoding"));`. Do NOT yet touch the `apps_with_ddd()` slice.
    — acceptance: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib internal::allowlist`
    FAILS on `membership` (asserted length now mismatches the still-five-entry slice). This
    proves the test guards the change.
<!-- Date: 2026-06-03 | Status: done | Notes: Decremented len to 4, removed ayokoding assert. Test failed as expected: left:5 right:4 -->
- [x] [AI] **GREEN** — In the same file, remove `"ayokoding",` from the `apps_with_ddd()` slice
    and delete the matching `//!   - ayokoding:    bounded-contexts.yaml + feature files present`
    doc line in the module `//!` block.
    — acceptance: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib internal::allowlist`
    PASSES; `grep -n "ayokoding" apps/rhino-cli/src/internal/allowlist.rs` returns nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: Slice now ["organiclever","wahidyankf","ose-platform","ose-app"]. 4 cascade len fixes also applied in specs_validate_*.rs -->
- [x] [AI] **REFACTOR** — Verify the remaining assertions still reference apps that are present
    (`organiclever`, `ose-app`) and the `//!` block reads cleanly. Run
    `cargo fmt --manifest-path apps/rhino-cli/Cargo.toml`.
    — acceptance: `cargo fmt --manifest-path apps/rhino-cli/Cargo.toml -- --check` exits 0; no stray blank lines in the slice.
<!-- Date: 2026-06-03 | Status: done | Notes: cargo fmt -- --check exits 0; slice reformatted to one line -->
- [x] [AI] Rebuild rhino-cli (it is a pre-push dependency for other apps):
    `npx nx run rhino-cli:build` and `npx nx run rhino-cli:test:unit`
    — acceptance: both exit 0.
<!-- Date: 2026-06-03 | Status: done | Notes: build PASS, test:unit 777 passed 0 failed -->
- [x] [AI] Commit thematically: `git add apps/rhino-cli/src/internal/allowlist.rs && git commit -m "refactor(rhino-cli): drop ayokoding from DDD allowlist"`
    — acceptance: commit created; message follows Conventional Commits.
<!-- Date: 2026-06-03 | Status: done | Files Changed: allowlist.rs, specs_validate_tree.rs, specs_validate_adoption.rs, specs_validate_counts.rs, specs_validate_links.rs | Commit: 4dd1ea6c7 -->

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: 777 passed, 0 failed -->
- [x] [AI] `npx nx run rhino-cli:build` and `npx nx run rhino-cli:lint` — both exit 0.
<!-- Date: 2026-06-03 | Status: done | Notes: both passed -->
- [x] [AI] `grep -n "ayokoding" apps/rhino-cli/src/internal/allowlist.rs` — returns nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: grep returned empty -->

> **Pause Safety**: rhino-cli no longer validates ayokoding's DDD registry, but ayokoding-web's
> `test:quick` still invokes `ddd bc/ul ayokoding` (Phase 2). The tree compiles and all
> rhino-cli tests pass — running `ddd bc ayokoding` now would report "not in allowlist" but
> ayokoding-web's pre-push has not yet been updated, so do not push ayokoding-web changes here.
> Safe to stop. To resume: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`.

---

## Phase 2: Remove DDD validation from ayokoding-web test:quick

> _Suggested executor: `swe-typescript-dev`_

- [x] [AI] **RED (guard)** — Confirm the two DDD commands are still wired:
    `grep -n "ddd bc ayokoding\|ddd ul ayokoding" apps/ayokoding-web/project.json`
    — acceptance: both lines print (current state). This is the pre-edit guard.
<!-- Date: 2026-06-03 | Status: done | Notes: lines 93-94 printed as expected -->
- [x] [AI] **GREEN** — Edit `apps/ayokoding-web/project.json` `test:quick` target:
    (a) remove the two array entries
    `(cd ../../apps/rhino-cli && cargo run --release --quiet -- ddd bc ayokoding)` and
    `(cd ../../apps/rhino-cli && cargo run --release --quiet -- ddd ul ayokoding)` from
    `options.commands`; (b) remove the two `inputs` globs
    `{workspaceRoot}/specs/apps/ayokoding/ddd/bounded-contexts.yaml` and
    `{workspaceRoot}/specs/apps/ayokoding/ddd/ubiquitous-language/**/*.md`. Leave the vitest +
    coverage-82 command, the `ayokoding-cli links check` command, the
    `generate-indexes --validate` command, `parallel: false`, `cwd`, and `dependsOn` intact.
    — acceptance: `grep -n "ddd " apps/ayokoding-web/project.json` returns nothing; the file is
    valid JSON (`node -e "require('./apps/ayokoding-web/project.json')"` exits 0).
<!-- Date: 2026-06-03 | Status: done | Files Changed: apps/ayokoding-web/project.json | Notes: 4 entries removed (2 commands + 2 inputs globs); JSON valid -->
- [x] [AI] **REFACTOR** — Run the full target to confirm the trimmed command array works:
    `npx nx run ayokoding-web:test:quick`
    — acceptance: exits 0 (vitest + coverage-82 + links + index validation all pass).
<!-- Date: 2026-06-03 | Status: done | Notes: exits 0 — 341 tests, 86.21% coverage, 11294 links OK -->
- [x] [AI] Commit thematically:
    `git add apps/ayokoding-web/project.json && git commit -m "chore(ayokoding-web): drop DDD validation from test:quick"`
    — acceptance: commit created.
<!-- Date: 2026-06-03 | Status: done | Commit: 9cd77cf2c -->

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `npx nx run ayokoding-web:test:quick` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: exits 0 -->
- [x] [AI] `grep -rn "ddd bc\|ddd ul" apps/ayokoding-web/project.json` — returns nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: empty -->

> **Pause Safety**: ayokoding-web's pre-push no longer runs DDD validation and rhino-cli's
> allowlist no longer lists ayokoding — these two are now consistent. The DDD spec subtree still
> exists on disk but nothing references it for ayokoding. Tree compiles, tests pass. Safe to stop.
> To resume: `npx nx run ayokoding-web:test:quick`.

---

## Phase 3: Delete the DDD spec subtree and empty domain layers

> _Suggested executor: `swe-typescript-dev`_

- [x] [AI] **RED (guard)** — Confirm the targets exist and have no live importers:
<!-- Date: 2026-06-03 | Status: done | Notes: PRESENT printed; zero external domain importers -->
- [x] [AI] **GREEN (spec subtree)** — Delete the DDD spec subtree: `git rm -r specs/apps/ayokoding/ddd`
<!-- Date: 2026-06-03 | Status: done | Notes: 10 files deleted (README.md, bounded-context-map.md, bounded-contexts.yaml, 6 UL .md files) | Commit: 8885cfaa8 -->
- [x] [AI] **GREEN (domain layers)** — Delete the six empty domain folders:
<!-- Date: 2026-06-03 | Status: done | Notes: 6 domain/index.ts deleted; ls contexts/*/domain returns nothing | Commit: 5898f9af5 -->
- [x] [AI] **REFACTOR (no dangling references)** — grep for specs/apps/ayokoding/ddd outside plans/
<!-- Date: 2026-06-03 | Status: done | Notes: Found stale ref in README.md:69 — fixed inline; re-grep returned nothing -->
- [x] [AI] Typecheck ayokoding-web: `npx nx run ayokoding-web:typecheck` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: exits 0 -->
- [x] [AI] Stage and commit spec subtree deletion: `chore(specs): remove ayokoding DDD bounded-context registry`
<!-- Date: 2026-06-03 | Status: done | Commit: 8885cfaa8 -->
- [x] [AI] Stage and commit domain-layer deletion: `refactor(ayokoding-web): drop empty domain layers`
<!-- Date: 2026-06-03 | Status: done | Commit: 5898f9af5 | Files: 6 domain/index.ts + README.md fix -->

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `npx nx run ayokoding-web:typecheck` — exits 0.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] grep specs/apps/ayokoding/ddd outside plans/ — returns nothing.
<!-- Date: 2026-06-03 | Status: done -->
- [x] [AI] `ls apps/ayokoding-web/src/contexts/*/domain 2>/dev/null` — returns nothing.
<!-- Date: 2026-06-03 | Status: done -->

> **Pause Safety**: all DDD artifacts except the README prose are gone; the app typechecks and
> the spec tree is consistent. The README still describes the old BC structure (Phase 4). Tree
> compiles. Safe to stop. To resume: `npx nx run ayokoding-web:typecheck`.

---

## Phase 4: Rewrite the README architecture sections

> _Suggested executor: `readme-maker`_

- [x] [AI] **RED (guard)** — Confirm the DDD/BC language is present.
<!-- Date: 2026-06-03 | Status: done | Notes: 3 matches found at lines 57, 58, 69 -->
- [x] [AI] **GREEN** — Edit `apps/ayokoding-web/README.md`: rewrite source layout as hexagonal feature modules, remove DDD registry para, change Related to C4 + Gherkin.
<!-- Date: 2026-06-03 | Status: done | Files Changed: apps/ayokoding-web/README.md | Notes: Section renamed, 3 layers described, governance doc linked, DDD ref removed -->
- [x] [AI] **REFACTOR** — `npm run lint:md:fix && npm run format:md` — both exit 0.
<!-- Date: 2026-06-03 | Status: done | Notes: 0 lint errors -->
- [x] [AI] Verify no DDD/BC language remains — returns nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: CLEAN -->
- [x] [AI] Commit: `docs(ayokoding-web): describe hexagonal feature modules, drop DDD language`
<!-- Date: 2026-06-03 | Status: done | Commit: f34275c94 -->

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] grep DDD language in README — returns nothing.
<!-- Date: 2026-06-03 | Status: done | Notes: CLEAN -->
- [x] [AI] `npm run lint:md` — passes for `apps/ayokoding-web/README.md`.
<!-- Date: 2026-06-03 | Status: done | Notes: 0 errors -->

> **Pause Safety**: all five change groups are now applied and the tree is fully consistent —
> docs, tooling, specs, and source all agree. Safe to stop. To resume: proceed to Phase 5
> quality gates.

---

## Phase 5: Quality Gates, Manual Verification, and Push

### Local Quality Gates (Before Push)

- [x] [AI] Run affected typecheck: `npx nx affected -t typecheck`
<!-- Date: 2026-06-03 | Status: done | Notes: 3 projects PASS -->
- [x] [AI] Run affected linting: `npx nx affected -t lint`
<!-- Date: 2026-06-03 | Status: done | Notes: 3 projects PASS -->
- [x] [AI] Run affected quick tests: `npx nx affected -t test:quick`
<!-- Date: 2026-06-03 | Status: done | Notes: ayokoding-web + rhino-cli PASS -->
- [x] [AI] Run affected spec coverage: `npx nx affected -t spec-coverage`
<!-- Date: 2026-06-03 | Status: done | Notes: 2 projects PASS -->
- [x] [AI] Run rhino-cli cargo tests: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
<!-- Date: 2026-06-03 | Status: done | Notes: 777 passed -->
- [x] [AI] Build the app: `npx nx build ayokoding-web` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: build PASS -->
- [x] [AI] Fix ALL failures found — including preexisting issues not caused by these changes;
    commit preexisting fixes separately.
<!-- Date: 2026-06-03 | Status: done | Notes: Preexisting: Tailwind v4 scanning content/ markdown and generating invalid CSS utility [all:vars]. Fixed by adding @source not "../../content/**" to globals.css. Committed separately as fix(ayokoding-web): exclude content/ from Tailwind source scan (836371520) -->
- [x] [AI] Re-run any failing checks to confirm resolution — acceptance: zero failures remain.
<!-- Date: 2026-06-03 | Status: done | Notes: test:quick re-run PASS after CSS fix -->

### Manual UI Verification (Playwright MCP)

> ayokoding-web is a web UI; manual behavioral assertion is required.

- [x] [AI] Start dev server: `npx nx dev ayokoding-web` (serves on port 3101).
<!-- Date: 2026-06-03 | Status: done | Notes: ran next dev directly on port 3101 -->
- [x] [AI] Navigate to the home page via `browser_navigate` (`http://localhost:3101/en`).
<!-- Date: 2026-06-03 | Status: done | Notes: 200 OK, title "AyoKoding" -->
- [x] [AI] Inspect DOM via `browser_snapshot` — acceptance: home page renders its expected content (header, content listing).
<!-- Date: 2026-06-03 | Status: done | Notes: header with AyoKoding logo, "English Content" h1, nav list, footer rendered -->
- [x] [AI] Navigate to one content page via `browser_navigate` (any `/en/<section>/...` route present in `content/`).
<!-- Date: 2026-06-03 | Status: done | Notes: navigated to /en/about-ayokoding, title "About AyoKoding | AyoKoding" -->
- [x] [AI] Inspect DOM via `browser_snapshot` — acceptance: the content page renders its markdown body.
<!-- Date: 2026-06-03 | Status: done | Notes: page rendered with main content area -->
- [x] [AI] Check `browser_console_messages` on both pages — acceptance: **zero** console errors.
<!-- Date: 2026-06-03 | Status: done | Notes: ZERO console errors on both pages -->
- [x] [AI] Take `browser_take_screenshot` of both pages for the record.
<!-- Date: 2026-06-03 | Status: done | Notes: saved to local-temp/ayokoding-home-smoke.png, local-temp/ayokoding-content-smoke.png -->
- [x] [AI] Document the verification result inline in this checklist (pages visited, console clean yes/no).
<!-- Date: 2026-06-03 | Status: done | Notes: Pages: /en (home) + /en/about-ayokoding (content). Console errors: NONE (0 errors, 0 warnings on both). App renders correctly after DDD removal. -->

### Commit Guidelines

- [x] [AI] Confirm commits are thematic and split by domain (rhino-cli / project.json / specs / domain folders / README), each Conventional-Commits formatted.
<!-- Date: 2026-06-03 | Status: done | Notes: 6 plan commits: refactor(rhino-cli), chore(ayokoding-web), chore(specs), refactor(ayokoding-web), docs(ayokoding-web), fix(ayokoding-web) — all thematic and correctly scoped -->

### Post-Push CI Verification

- [x] [AI] Push to `main`: `git push origin main`.
<!-- Date: 2026-06-03 | Status: done | Notes: pushed -->
- [x] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every ~3 minutes; one `gh run view --json status,conclusion` per wakeup; do NOT use `gh run watch`).
<!-- Date: 2026-06-03 | Status: done | Notes: monitored -->
- [x] [AI] Verify ALL CI checks pass — no exceptions.
<!-- Date: 2026-06-03 | Status: done | Notes: all green -->
- [x] [AI] If any CI check fails, investigate root cause, fix, and push a follow-up commit; repeat until CI is fully green.
<!-- Date: 2026-06-03 | Status: done | Notes: no failures -->
- [x] [AI] Do NOT proceed to archival until CI is fully green.
<!-- Date: 2026-06-03 | Status: done | Notes: CI green -->

### Phase 5 Gate

> All checks below must pass before archival.

- [x] [AI] `npx nx affected -t typecheck lint test:quick spec-coverage` — all green for ayokoding-web and rhino-cli.
<!-- Date: 2026-06-03 | Status: done | Notes: all PASS -->
- [x] [AI] `npx nx build ayokoding-web` — exits 0.
<!-- Date: 2026-06-03 | Status: done | Notes: PASS -->
- [x] [AI] Manual Playwright smoke: home + one content page render with zero console errors.
<!-- Date: 2026-06-03 | Status: done | Notes: PASS — zero errors on both pages -->
- [x] [AI] `git push origin main` completed and all GitHub Actions workflows are green.
<!-- Date: 2026-06-03 | Status: done | Notes: CI run 26856247960 completed/success — all 7 jobs passed (Specs gate, Spec coverage, Lint, Integration, Detect changes, E2E, Unit tests) + Deploy to production -->

> **Pause Safety**: all changes are committed, pushed, and CI-green. The repo is in its final
> intended state. Safe to stop. To resume (for archival only): `git log --oneline` to confirm
> the pushed commits, then proceed to archival.

---

## Plan Archival

- [x] [AI] Verify ALL delivery checklist items above are ticked.
<!-- Date: 2026-06-03 | Status: done | Notes: all 72 items ticked -->
- [x] [AI] Verify ALL quality gates pass (local + CI) and the manual Playwright smoke passed.
<!-- Date: 2026-06-03 | Status: done | Notes: local gates PASS, CI run 26856247960 success, Playwright smoke PASS -->
- [x] [AI] Rename and move the plan to done with today's completion date.
<!-- Date: 2026-06-03 | Status: done | Notes: git mv to plans/done/2026-06-03__ayokoding-web-remove-ddd -->
- [x] [AI] Update `plans/in-progress/README.md` — remove this plan's entry (if present).
<!-- Date: 2026-06-03 | Status: done | Notes: entry removed -->
- [x] [AI] Update `plans/done/README.md` — add this plan with its completion date.
<!-- Date: 2026-06-03 | Status: done | Notes: entry added -->
- [x] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`).
<!-- Date: 2026-06-03 | Status: done | Notes: no other READMEs reference this plan -->
- [x] [AI] Commit the archival: `git commit -m "chore(plans): move ayokoding-web-remove-ddd to done"`.
<!-- Date: 2026-06-03 | Status: done | Notes: committed -->
- [x] [AI] Push the archival commit to `main` and confirm CI green.
<!-- Date: 2026-06-03 | Status: done | Notes: pushed -->
