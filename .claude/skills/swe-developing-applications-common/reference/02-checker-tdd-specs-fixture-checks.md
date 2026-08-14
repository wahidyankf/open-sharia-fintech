# swe-code-checker Validation Steps 6.5-6.8

TDD compliance, specs/Gherkin completeness, regression-test mandate, and git-fixture isolation —
run for every code change or project under review.

## Step 6.5: TDD Compliance

Reference: `repo-governance/development/workflow/test-driven-development.md`.

- **Test-first evidence**: does every non-trivial change have accompanying tests? Are plan
  delivery-checklist steps TDD-shaped (failing test → implement → refactor), not "implement then
  test"? Are all business-logic paths unit-tested? HIGH when tests are absent for new behavior;
  MEDIUM when tests exist but look written after the fact (all pass trivially on first run, no
  obvious red phase).
- **Test level appropriateness**: is the behavior tested at the cheapest level that meaningfully
  exercises it (pure-function bugs → unit, not E2E; persistence bugs → integration, not mocked
  unit; user-visible flow bugs → E2E plus manual-verification notes)? MEDIUM when the wrong level
  is used.
- **Manual verification shape**: manual verification must be a written, dated, repeatable script
  with discrete expected observations — unstructured "tested manually" notes are a finding. MEDIUM
  when undocumented; HIGH when a recurring behavior has only informal notes and no automated
  coverage plan.

**Findings format**:

```markdown
### Finding: TDD Compliance

**Project**: [project-name]
**File**: [file-path or delivery checklist path]
**Criticality**: HIGH | MEDIUM
**Confidence**: HIGH | MEDIUM | FALSE_POSITIVE

**Issue**: [tests missing / wrong level / manual verification unstructured]
**Standard**: [Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md)
**Recommendation**: [write failing test first; move to cheaper level; structure manual script]
```

## Step 6.6: Specs & Gherkin Completeness (Direct-Code Path)

Reference: [Feature Change Completeness Convention §Two Paths](../../../repo-governance/development/quality/feature-change-completeness.md)
— the direct-change-without-plan counterpart to `plan-checker` Step 5j.

- **Companion Gherkin present**: any `apps/**`/`libs/**` change altering observable behavior
  (new/changed/removed endpoint, command, procedure, component, user-facing behavior) needs a
  matching `.feature` add/update under `specs/apps/**`/`specs/libs/**`. HIGH if absent; MEDIUM if
  the spec exists but is stale (doesn't reflect the new behavior).
- **specs:coverage wired and green**: the project must have a `specs:coverage` target and it must
  pass (`rhino-cli specs behavior-coverage validate`) — HIGH if a behavior change breaks it.
- **Pure-refactor exemption**: behavior-preserving refactors, dependency bumps without behavior
  change, and config-only edits are exempt per the applicability table — never flag these.

## Step 6.7: Regression Test Mandate (Bug/Regression Fixes)

Reference: [Regression Test Mandate](../../../repo-governance/development/quality/regression-test-mandate.md).

A `fix(...)` commit or any diff correcting wrong observable behavior MUST land with a reproducing
test in the same change set (fails before the fix, passes after) — blocking, no exemption, applies
to every defect type including cosmetic/visual. Form adapts to the defect: behavioural/functional →
a `specs/**` Gherkin scenario plus the consuming unit/integration/e2e test (per the
[Three-Level Testing Standard](../../../repo-governance/development/quality/three-level-testing-standard.md));
visual/design/UI → a DOM/computed-style or component test (or a Gherkin scenario for the on-design
expectation); content/copy/i18n → a test asserting the corrected string/translation. HIGH when
missing — unlike Step 6.6, the pure-refactor exemption never applies (a fix by definition changes
behavior to correct it).

## Step 6.8: Git Fixture Isolation

Reference: [Git Fixture Isolation Convention](../../../repo-governance/development/quality/git-fixture-isolation.md).

For any test/fixture (any language) invoking a raw `git` subprocess to create or mutate a
**throwaway** repository (`git init`, `commit`, `config`, `worktree add`, `branch`, `checkout -b`,
`reset --hard`, or equivalents), verify all six mandatory isolation layers: (1)
`GIT_CEILING_DIRECTORIES` set to the fixture's temp root; (2) explicit `GIT_DIR` set — no reliance
on `current_dir()`/process CWD (`GIT_WORK_TREE` is context-dependent, not mandatory — it must be
_absent_ for `git worktree add` and the escape guard, so its absence alone is never a finding); (3)
`GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null`; (4) a pre-write escape guard
(canonicalized `git rev-parse --show-toplevel` compared against the intended tempdir, failing loud
on mismatch) before every write subcommand; (5) a real exit-status check
(`status.success()`/language equivalent) on every `git` subprocess — a bare `.expect()`/try-catch
around the spawn alone does not satisfy this, since it only catches spawn failures, not `git`
itself returning non-zero; (6) never diagnosing this fixture class in the primary/real worktree
(throwaway clone only) — a process rule, out of scope for static checks.

Starting grep: `rg -l 'Command::new\("git"\)|exec\.Command\("git"|child_process\.(spawn|exec(File)?)\("git"|subprocess\.(run|Popen)\(\s*\[?"git"|ProcessStartInfo\(.*"git"' -g '*test*' -g '*fixture*' -g '*spec*'`
— for each match, confirm layers 1-5 appear in the same function or a shared helper it calls.

**Criticality**: CRITICAL — this is the exact gap class that let a real fixture repeatedly corrupt
the primary repository (stray commits on the real branch, overwritten local git identity) in the
motivating incident. Missing isolation layers are a live data-loss/repo-corruption risk, not style.
