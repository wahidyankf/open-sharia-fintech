# Delivery Checklist: Harden `ayokoding-www-fe-e2e` Bulk-Link-Check Concurrency

**Delivery Mode**: `worktree-to-pr` (the repo default). One delivery unit, one PR.

## Phase 0: Baseline

- [ ] [AI] Confirm the two named step files still contain the unbounded-`Promise.all` pattern
      described in `tech-docs.md` (re-verify — this backlog item may sit unexecuted for a while and
      the pattern may have already changed) — acceptance: pattern confirmed present, or this plan is
      closed as moot if it's already been fixed by other means.
- [ ] [AI] Run `npx nx run ayokoding-www-fe-e2e:test:e2e` 2-3 times to re-baseline the observed flake
      rate before making any change — acceptance: baseline recorded (pass/fail per run).

### Phase 0 Gate

- [ ] [AI] Baseline recorded; pattern confirmed present or plan closed as moot.

---

## Phase 1: Shared Concurrency-Bounded Link-Check Helper (TDD)

- [ ] [AI] **RED**: `apps/ayokoding-www-fe-e2e/src/steps/support/check-links-resolve.test.ts` —
      assert that, given more hrefs than the configured batch size and fake slow-responding request
      fn, in-flight requests never exceed the batch size — acceptance: fails (helper doesn't exist
      yet).
- [ ] [AI] **GREEN**: implement `checkLinksResolve(requestFn, hrefs, opts)` in
      `check-links-resolve.ts` — batches requests at a fixed concurrency limit, retries a single
      transport-layer failure once (see tech-docs.md Open Decisions for batch size/retry-backoff
      resolution) — acceptance: RED test passes.
- [ ] [AI] **REFACTOR**: extract the retry-classification logic (which errors are
      transport-layer vs. assertion failures) into its own named predicate for clarity — acceptance:
      tests still pass, no behavior change.
- [ ] [AI] Companion Gherkin: add or extend
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` scenarios per
      `prd.md`'s three acceptance-criteria scenarios (per the Specs & Gherkin Completeness rule) —
      acceptance: `specs:behavior:coverage` covers the new scenarios.

### Phase 1 Gate

- [ ] [AI] `checkLinksResolve` implemented, unit-tested, Gherkin-covered.
- [ ] [AI] `typecheck`, `lint`, `test:quick`, `test:unit` exit 0 for `ayokoding-www-fe-e2e`.

---

## Phase 2: Apply to Both Step Files and Verify

- [ ] [AI] Replace the `Promise.all` block in `ia-navigation-revamp.steps.ts` (both call sites) with
      `checkLinksResolve` — acceptance: same assertions, same messages, no behavior change to what
      counts as pass/fail.
- [ ] [AI] Replace the `Promise.all` block in `course-rehome-redirects.steps.ts` with
      `checkLinksResolve` — acceptance: same as above.
- [ ] [AI] Run `npx nx run ayokoding-www-fe-e2e:test:e2e` at least 5 times in a row (ideally
      alongside other concurrent `nx affected` load, matching the conditions that originally
      surfaced the flake) — acceptance: 5/5 clean passes with the same 578/759 (or current) pass
      count; zero network-layer failures.
- [ ] [AI] Re-run the two-file diff against `git diff --stat` to confirm no other files changed —
      acceptance: only the three files above (`check-links-resolve.ts` + its test +
      the two step files) changed.

### Phase 2 Gate

- [ ] [AI] 5/5 clean runs recorded as evidence in this section.
- [ ] [AI] Full affected suite (`typecheck lint test:quick test:unit test:integration test:e2e
specs:behavior:coverage`) exits 0.
- [ ] [AI] Draft PR opened, 3-cycle PR-Review Maker→Fixer loop run, all 5 hardened merge
      preconditions hold, `[AI]`-merged to `main`.

---

## Phase 3: Knowledge Capture

- [ ] [AI] Triage `learnings.md` per the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
      — route or discard every entry, or record the explicit "none" escape.

### Phase 3 Gate

- [ ] [AI] Every `learnings.md` entry terminal.
- [ ] [AI] Plan folder moved to `plans/done/YYYY-MM-DD__harden-ayokoding-www-fe-e2e-bulk-link-concurrency/`.
