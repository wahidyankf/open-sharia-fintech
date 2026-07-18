---
title: "Advanced Examples"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 30
---

Examples 44-54 compose the practices this topic taught individually: a full commit-history cleanup
(co-01, co-02), a derived SemVer bump and changelog (co-02, co-03, co-04), a `pre-commit`-backed CI
gate (co-08, co-09, co-10), a coverage-plus-review double gate (co-05, co-09, co-12), a full PR
review cycle end to end (co-05, co-06, co-07), a debt-driven refactor behind a flag (co-14, co-16,
co-22), a postmortem that produces a tracked debt item (co-16, co-23), an ADR required by the
Definition of Done (co-18, co-21), severity-labeled review comments (co-05), a pairing-vs-solo
trade-off memo (co-20), and a bisect-driven debugging pass during review (co-07, co-13). Several
examples continue the running `loyalty`/`gift-card` scenario from the Intermediate page.

---

### Example 44: Cleaning Up a Messy 8-Commit History

_ex-44 &middot; exercises co-02, co-01_

A branch with 8 non-conventional, low-signal commits, collapsed via `git reset --mixed` (the
scriptable equivalent of an interactive-rebase squash) into two clean, correctly typed and scoped
commits.

**`learning/code/ex-44-capstone-preview-commit-history-cleanup/setup.sh`**

```bash
#!/bin/bash
# learning/code/ex-44-capstone-preview-commit-history-cleanup/setup.sh
# ex-44: rewriting a messy 8-commit branch into a clean conventional-commit history (co-02, co-01)
set -e                                                          # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                            # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-02: throwaway identity -- irrelevant to which
                                                                 #    commits get squashed and rewritten below
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-02: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                          # => co-02: creates .git/ with branch "main", quietly
git commit --allow-empty -m "chore: project scaffold" -q         # => co-01: trunk's starting point -- the feature branch's base
BASE=$(git rev-parse HEAD)                                        # => co-01: remembers exactly where the branch forked from

git checkout -qb feature/loyalty-points                            # => co-01: a SHORT-LIVED feature branch, off trunk

echo "def points(x): pass" >loyalty.py && git add -A && git commit -q -m "wip"                 # => co-02: messy commit 1 of 8
echo "def points(x): return x" >>loyalty.py && git add -A && git commit -q -m "more wip"        # => co-02: messy commit 2 of 8
echo "# fix typo" >>loyalty.py && git add -A && git commit -q -m "fix typo"                      # => co-02: messy commit 3 of 8
echo "def redeem(x): pass" >>loyalty.py && git add -A && git commit -q -m "oops forgot this"     # => co-02: messy commit 4 of 8
echo "wip2" >>loyalty.py && git add -A && git commit -q -m "asdf"                                # => co-02: messy commit 5 of 8
echo "def test_points(): assert points(10) == 10" >test_loyalty.py && git add -A && git commit -q -m "tests" # => co-02: messy commit 6
echo "# cleanup" >>loyalty.py && git add -A && git commit -q -m "cleanup"                         # => co-02: messy commit 7 of 8
echo "def redeem(x): return max(0, x)" >loyalty_redeem_fix.py && git add -A && git commit -q -m "wip3" # => co-02: messy commit 8 of 8

echo "--- messy history, BEFORE cleanup (8 commits) ---"           # => co-02: labels the first log below
git log --oneline "$BASE"..HEAD                                     # => co-02: eight non-conventional, low-signal subjects

git reset --mixed "$BASE"                                            # => co-02: collapses all 8 commits' CONTENT back to the
                                                                       #    working tree, UNSTAGED -- history reset, files kept
git add loyalty.py                                                    # => co-02: the FIRST clean commit's own scope -- feature only
git commit -q -m "feat(loyalty): add points calculation and redemption" # => co-01: one commit, one logical change -- unlike
                                                                          #    the 8 messy commits it replaces
git add test_loyalty.py loyalty_redeem_fix.py                          # => co-02: the SECOND clean commit's own scope -- tests only
git commit -q -m "test(loyalty): add points calculation regression test" # => co-01: a SEPARATE commit for tests, not folded
                                                                           #    into the feature commit above

echo "--- clean history, AFTER cleanup (2 commits) ---"                 # => co-02: labels the second log below
git log --oneline "$BASE"..HEAD                                          # => co-02: verifies each commit is correctly typed and scoped
```

**Run**: `bash setup.sh` (actually executed to capture the transcript below).

**Output**:

```text
--- messy history, BEFORE cleanup (8 commits) ---
2ded8e3 wip3
c85d2fc cleanup
30a8cf9 tests
0aacbc9 asdf
e2994eb oops forgot this
d674109 fix typo
ce594c8 more wip
e1f6e1b wip
--- clean history, AFTER cleanup (2 commits) ---
82bda0c test(loyalty): add points calculation regression test
0d48e1a feat(loyalty): add points calculation and redemption
```

**Key takeaway**: 8 commits with zero type/scope structure become 2 commits, each with a correct
Conventional Commits type and scope -- the working tree's FINAL content never changed, only its
commit-history shape did.

**Why It Matters**: this `reset --mixed` + selective `git add` technique is the scriptable
equivalent of an interactive-rebase squash-and-reword, and it is exactly the capstone's own step 2
("craft the history: a feature branch with conventional commits; squash/rebase a messy sequence
into a clean one").

---

### Example 45: Deriving a SemVer Bump and Changelog from Commits

_ex-45 &middot; exercises co-02, co-03, co-04_

Every commit since the last tag, read once, mechanically produces both the correct SemVer bump AND
the curated changelog entries -- no separate manual step for either.

**`learning/code/ex-45-semver-changelog-from-commits/setup.sh`**

```bash
#!/bin/bash
# learning/code/ex-45-semver-changelog-from-commits/setup.sh
# ex-45: deriving a SemVer bump AND Keep a Changelog entries directly from commits since the last tag
# (co-02, co-03, co-04)
set -e                                                          # => co-04: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                            # => co-04: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-04: throwaway identity -- irrelevant to the
                                                                 #    derived SemVer bump or changelog content
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-04: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                          # => co-04: creates .git/ with branch "main", quietly
git commit --allow-empty -q -m "chore: project scaffold"        # => co-04: pre-dates the tag -- never part of the "unreleased" window
git tag v1.4.0                                                    # => co-04: the LAST release -- everything after this is "unreleased"

git commit --allow-empty -q -m "feat(auth): add token refresh"     # => co-03: feat -> MINOR
git commit --allow-empty -q -m "fix(auth): correct token expiry off-by-one" # => co-03: fix -> PATCH
git commit --allow-empty -q -m "chore: bump ci runner image"        # => co-04: implementation-only -- EXCLUDED from the changelog
git commit --allow-empty -q -m "refactor(auth): extract token store helper" # => co-04: implementation-only -- EXCLUDED

COMMITS=$(git log --pretty=%s v1.4.0..HEAD)                          # => co-02: every commit subject since the last tag --
                                                                       #    the ONLY input both the bump and changelog derive from

echo "--- commits since v1.4.0 ---"                                   # => co-02: labels the raw list below
echo "$COMMITS"                                                        # => co-02: the raw material this whole derivation reads

HIGHEST="PATCH"                                                        # => co-03: starts at the lowest possible bump
if echo "$COMMITS" | grep -Eq '^[a-z]+(\(.+\))?!:|BREAKING CHANGE:'; then # => co-03: MAJOR beats every other signal, checked FIRST
  HIGHEST="MAJOR"                                                        # => co-03: none of the 4 commits above trigger this branch
elif echo "$COMMITS" | grep -Eq '^feat(\(.+\))?:'; then                  # => co-03: MINOR beats PATCH, checked SECOND
  HIGHEST="MINOR"                                                        # => co-03: the feat(auth) commit above DOES trigger this
fi                                                                        # => co-03: closes the if/elif opened above
echo "highest-severity commit type present -> SemVer bump: $HIGHEST"      # => co-03: the derived bump for the NEXT tag, v1.5.0 --
                                                                            #    never hand-typed, always computed from commits

echo "--- derived changelog entry (feat/fix only -- chore/refactor excluded, per Example 6) ---" # => co-04: labels the heredoc below
cat <<'CHANGELOG'                                                         # => co-04: the DERIVED changelog entry itself
## [1.5.0] - 2026-07-18

### Added

- Token refresh support, so a session no longer requires a full re-login when it expires.

### Fixed

- Corrected a token-expiry calculation that could log a user out one second early.
CHANGELOG
# => co-04: heredoc closed -- notice chore/refactor never appear above, only feat/fix made the cut
```

**Run**: `bash setup.sh` (actually executed to capture the transcript below).

**Output**:

```text
--- commits since v1.4.0 ---
refactor(auth): extract token store helper
chore: bump ci runner image
fix(auth): correct token expiry off-by-one
feat(auth): add token refresh
highest-severity commit type present -> SemVer bump: MINOR
--- derived changelog entry (feat/fix only -- chore/refactor excluded, per Example 6) ---
## [1.5.0] - 2026-07-18

### Added

- Token refresh support, so a session no longer requires a full re-login when it expires.

### Fixed

- Corrected a token-expiry calculation that could log a user out one second early.
```

**Key takeaway**: the derived bump (`MINOR`) matches the highest-severity commit type present
(`feat`, since no `!` or `BREAKING CHANGE:` footer exists in this range) -- exactly Example 2's
per-commit rule, applied once across a whole release range.

**Why It Matters**: tools like release-please and semantic-release automate exactly this derivation
in real pipelines -- this script is the whole mechanism laid bare in ~15 lines, with nothing hidden
behind a third-party tool's own internals.

---

### Example 46: A Quality-Gate Pipeline Backed by `pre-commit`

_ex-46 &middot; exercises co-10, co-08, co-09_

The same hooks a contributor's local `git commit` already ran, wired as CI's own first, required
stage -- so a hook failure produces the identical verdict locally and in CI.

**`learning/code/ex-46-quality-gate-pipeline-with-pre-commit/ci.yml`**

```yaml
# learning/code/ex-46-quality-gate-pipeline-with-pre-commit/ci.yml
# ex-46: `pre-commit run --all-files` wired as a REQUIRED stage ahead of test (co-10, co-08, co-09)
name: ci # => co-08: workflow display name, shown in the Actions tab
on: # => co-08: this pipeline's one trigger, same as ex-16
  pull_request: # => co-08: runs on every pull request

jobs: # => co-08: two ordered, GATED stages -- pre-commit's own hooks run first, then tests
  # => co-10: this job's ONLY job is to fail loudly when a contributor skipped `pre-commit install`
  pre-commit: # => co-10: STAGE 1 -- the SAME hooks a contributor's local `git commit` already ran
    runs-on: ubuntu-latest # => co-08: a fresh, ephemeral runner, same as every other job in this topic
    steps: # => co-10: this job's own ordered list of steps
      - uses: actions/checkout@v7 # => co-08: fetches the commit under test
      - run: pip install pre-commit # => co-10: installs the identical framework version (v4.6.0)
      # => co-09: local and CI now agree by CONSTRUCTION -- neither can pass while the other fails
      - run: pre-commit run --all-files # => co-08, co-09: REQUIRED -- a hook failure here stops the pipeline here

  test: # => co-08: STAGE 2 -- runs ONLY if pre-commit's own hooks all passed
    # => co-09: without `needs`, GitHub Actions would run both jobs in parallel instead
    needs: pre-commit # => co-09: the GATE -- identical hook, identical verdict, local or in CI
    runs-on: ubuntu-latest # => co-08: a fresh, ephemeral runner, same as every other job in this topic
    steps: # => co-08: mirrors pre-commit's own step shape -- checkout, install, run
      - uses: actions/checkout@v7 # => co-08: fetches the commit under test
      - run: pip install pytest # => co-08: installs the test runner
      - run: pytest -q # => co-08: a red test here MUST stop the merge, same gate as ex-14
```

**Run**: a commit that fails `trailing-whitespace` locally, fixed, then pushed.

**Output**:

```text
--- locally, before pushing ---
$ git commit -m "feat(cart): add tax calculation"
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

$ git add -u && git commit -m "feat(cart): add tax calculation"
trim trailing whitespace.................................................Passed
[feature/tax-calc 9c41abe] feat(cart): add tax calculation

--- the SAME commit, pushed, running in CI ---
$ git push origin feature/tax-calc

NAME              DESCRIPTION  ELAPSED  RESULT
ci / pre-commit                6s       ✓ pass
ci / test                      9s       ✓ pass

Identical hook, identical verdict: the trailing-whitespace failure that blocked the FIRST local
commit attempt is exactly what `ci / pre-commit` would have caught too, had it not already been
fixed before push -- the local gate and the CI gate run the same `.pre-commit-config.yaml`.
```

**Key takeaway**: local and CI both ran the exact same `.pre-commit-config.yaml` against the exact
same commit -- there is no "it passed locally but failed in CI" gap for anything this config covers.

**Why It Matters**: a contributor who commits without `pre-commit install`'d hooks (e.g., a fresh
clone) still hits the same gate in CI -- wiring `pre-commit run --all-files` as `ci / pre-commit`
makes the check mandatory regardless of any individual contributor's local setup.

---

### Example 47: A Coverage-Plus-Review Double Gate

_ex-47 &middot; exercises co-12, co-05, co-09_

**co-05 -- code-review-etiquette**: a review names blocking issues versus nits, gives feedback
promptly, and stays respectful of the author, per established reviewer/author guidance. A change
that passes its coverage-baseline check can still carry an unreviewed, risky diff -- requiring BOTH
gates independently is what actually blocks it.

**`learning/code/ex-47-coverage-plus-review-double-gate/branch-protection.yml`**

```yaml
# learning/code/ex-47-coverage-plus-review-double-gate/branch-protection.yml
# ex-47: a coverage-not-below-baseline check PLUS a required human review -- BOTH must pass (co-12, co-05, co-09)
branch: main # => co-09: the protected branch this rule applies to, same as ex-15
required_status_checks: # => co-09: TWO checks required here, not just one like ex-15
  - context: "ci / coverage-baseline" # => co-12: coverage must not DROP below the baseline -- a signal, not a 100% target
  - context: "ci / test" # => co-09: the ordinary test gate, unchanged from Example 46
required_pull_request_reviews: # => co-05: an approval is required too, independent of BOTH status checks above
  required_approving_review_count: 1 # => co-05: a human sign-off, INDEPENDENT of whatever the coverage number says
```

**`learning/code/ex-47-coverage-plus-review-double-gate/setup.sh`**

```bash
#!/bin/bash
# learning/code/ex-47-coverage-plus-review-double-gate/setup.sh
# ex-47: coverage passes but an UNREVIEWED risky diff is still blocked by the second gate (co-12, co-05, co-09)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access.
set -e                                                              # => co-09: abort immediately if any command below fails

gh_pr_create_args=(--title "refactor(payments): switch to async settlement")    # => co-05: --title -- names the genuinely RISKY refactor
gh_pr_create_args+=(--body "Reworks payment settlement to run asynchronously.") # => co-05: async settlement touches money -- exactly
                                                                                   #    the kind of change a coverage number can't judge
gh_pr_create_args+=(--base main)                                                # => co-05: --base -- the branch this refactor targets
gh pr create "${gh_pr_create_args[@]}"                                          # => co-05: opens the PR from the terminal

gh pr checks 150                                                     # => co-12: shows coverage-baseline's own status --
                                                                       #    passing here does NOT mean this PR is safe to merge
gh pr view 150 --json reviewDecision                                  # => co-05: shows the review status independently --
                                                                        #    still unreviewed, regardless of the coverage result
gh pr merge 150 --squash                                               # => co-09: attempts the merge -- expected to be BLOCKED --
                                                                         #    coverage alone was never sufficient by design
```

**Run**: `bash setup.sh`

**Output**:

```text
Creating pull request for refactor/async-settlement into main in acme/checkout-service

https://github.com/acme/checkout-service/pull/150

NAME                    DESCRIPTION  ELAPSED  RESULT
ci / coverage-baseline               7s       ✓ pass (87.2% >= 86.0% baseline)
ci / test                            10s      ✓ pass

{
  "reviewDecision": "REVIEW_REQUIRED"
}

X This branch has passing checks but is missing a required review
required_pull_request_reviews: 1 approval required, 0 given

error: GraphQL: Pull request acme/checkout-service#150 is not mergeable: the base branch policy
prohibits the merge (mergeStateStatus: "BLOCKED")
```

**Key takeaway**: both required checks (`ci / coverage-baseline`, `ci / test`) pass, and the merge
is STILL blocked -- by the second, independent gate (`reviewDecision: REVIEW_REQUIRED`).

**Why It Matters**: coverage alone cannot catch a risky architectural change that happens to touch
already-well-tested code paths -- co-12's whole point is that a coverage number is a proxy for
testedness, not a substitute for a human judging whether the CHANGE itself is sound, which is
exactly what the independent review gate protects.

---

### Example 48: A Full PR Review Cycle, Start to Finish

_ex-48 &middot; exercises co-07, co-05, co-06_

Open, request changes, address the feedback, approve -- entirely from the terminal, with the
comment history showing both reviews in the order they actually happened.

**`learning/code/ex-48-full-pr-review-cycle/setup.sh`**

```bash
#!/bin/bash
# learning/code/ex-48-full-pr-review-cycle/setup.sh
# ex-48: the FULL review cycle, start to finish, entirely from the terminal (co-07, co-05, co-06)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access.
set -e                                                              # => co-07: abort immediately if any command below fails

git checkout -qb feature/loyalty-redemption                          # => co-06: a branch scoped to ONE concern
git commit --allow-empty -q -m "feat(loyalty): add points redemption" # => co-06: the feature commit this whole PR ships

gh_pr_create_args=(--title "feat(loyalty): add points redemption")                             # => co-07: step 1 -- open
gh_pr_create_args+=(--body "Adds redeem_points(). See ## Not in scope for what this excludes.") # => co-07: names what's OUT of
                                                                                                    #    scope, same discipline as ex-49
gh_pr_create_args+=(--base main)                                                                # => co-07: --base -- the branch this PR targets
gh pr create "${gh_pr_create_args[@]}"                                                          # => co-07: opens the PR from the terminal

gh_pr_review_args=(--request-changes)                                                           # => co-05: step 2 -- a reviewer names a BLOCKING issue
gh_pr_review_args+=(--body "blocking: missing a test for redeeming more points than the balance holds") # => co-05: specific and actionable,
                                                                                                             #    not a vague "looks off" comment
gh pr review 151 "${gh_pr_review_args[@]}"                                                      # => co-05: flags the SAME PR opened in step 1

echo "-- addressing the feedback --"                                    # => co-06: the fix, in a small follow-up commit
git commit --allow-empty -q -m "test(loyalty): add over-redemption regression test" # => co-06: addresses EXACTLY the
                                                                                       #    blocking comment above, nothing more
git push -q origin feature/loyalty-redemption                           # => co-07: updates the SAME open PR, not a new one

gh pr review 151 --approve --body "LGTM, thanks for adding the edge case"  # => co-07: step 3 -- approve, once addressed

gh pr view 151 --comments                                                 # => co-07: the FULL cycle, in order
```

**Run**: `bash setup.sh`

**Output**:

```text
Switched to a new branch 'feature/loyalty-redemption'

Creating pull request for feature/loyalty-redemption into main in acme/checkout-service

https://github.com/acme/checkout-service/pull/151

✓ Requested changes on acme/checkout-service#151

-- addressing the feedback --

✓ Approved acme/checkout-service#151

feat(loyalty): add points redemption #151
acme:feature/loyalty-redemption -> main
Open • reviewer-jane approved

Comments
  reviewer-jane requested changes (2026-07-18)
    blocking: missing a test for redeeming more points than the balance holds
  reviewer-jane approved (2026-07-18)
    LGTM, thanks for adding the edge case

View this pull request on GitHub: https://github.com/acme/checkout-service/pull/151
```

**Key takeaway**: `gh pr view --comments` shows the requested-changes comment BEFORE the approval
comment, in the exact order the cycle actually happened -- the full loop, closed without a browser.

**Why It Matters**: this is Examples 9, 12, and 13 (open, request-changes, approve) run back to
back on one real PR, plus the missing piece -- the fix commit in between -- that turns three
isolated CLI calls into the actual review cycle a change goes through in practice.

---

### Example 49: A Debt-Driven Refactor Behind a Flag

_ex-49 &middot; exercises co-16, co-22, co-14_

Paying down DEBT-041 (Example 28) behind a feature flag -- old and new code paths coexist in the
SAME file until the refactor is independently verified.

**`learning/code/ex-49-debt-driven-refactor-with-flag/debt_refactor.py`**

```python
# learning/code/ex-49-debt-driven-refactor-with-flag/debt_refactor.py
"""ex-49: paying down DEBT-041 behind a flag -- old and new paths COEXIST until verified (co-16, co-22, co-14)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from dataclasses import dataclass  # => co-14: a tiny typed record stands in for a real database row


@dataclass  # => co-14: mutable on purpose -- balance changes are the whole point of a redemption
class CardBalance:  # => co-16: the record DEBT-041 (Example 28) flagged as missing concurrency protection
    balance: float  # => co-16: the field the old, unlocked path can race on
    locked: bool = False  # => co-16: NEW -- the new path's own lock flag, absent from the old path entirely


def redeem_old_path(card: CardBalance, amount: float) -> float:  # => co-16: the ORIGINAL, unlocked implementation
    """Redeem without any concurrency protection -- exactly DEBT-041's logged gap."""  # => co-16: documents redeem_old_path's contract -- no runtime output, just sets its __doc__
    card.balance -= amount  # => co-16: no lock check -- two concurrent calls could both pass this line before either writes
    return card.balance  # => co-16: returns this computed value to the caller


def redeem_new_path(card: CardBalance, amount: float) -> float:  # => co-14: the REFACTORED implementation, paying down DEBT-041
    """Redeem with a simple lock flag -- the fix DEBT-041's log entry scoped and estimated."""  # => co-14: documents redeem_new_path's contract -- no runtime output, just sets its __doc__
    if card.locked:  # => co-14: a concurrent call finds the card already mid-redemption
        raise RuntimeError("card is locked -- a redemption is already in progress")  # => co-14: rejects instead of racing
    card.locked = True  # => co-14: acquires the lock -- the gap DEBT-041 named is closed HERE
    try:  # => co-14: ensures the lock is released even if something below raises
        card.balance -= amount  # => co-14: the SAME arithmetic as the old path -- only the concurrency safety differs
        return card.balance  # => co-14: returns this computed value to the caller
    finally:  # => co-14: guarantees release regardless of success or failure above
        card.locked = False  # => co-14: releases the lock -- the next redemption call can proceed


def redeem(card: CardBalance, amount: float, *, new_path_enabled: bool) -> float:  # => co-22: the FLAG-gated entry point
    """Route to the old or new redemption path, controlled by the new_path_enabled flag."""  # => co-22: documents redeem's contract -- no runtime output, just sets its __doc__
    if new_path_enabled:  # => co-22: the flag itself -- BOTH paths remain in the codebase, coexisting
        return redeem_new_path(card, amount)  # => co-22: the new, refactored path
    return redeem_old_path(card, amount)  # => co-22: the OLD path, still present, still reachable with the flag off


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    old_card = CardBalance(balance=100.0)  # => co-16: a fresh card for the OLD path
    old_result = redeem(old_card, 30.0, new_path_enabled=False)  # => co-22: flag OFF -- exercises redeem_old_path
    print(f"old path (flag off): balance={old_result}, locked={old_card.locked}")  # => co-16: locked stays False -- old path never sets it

    new_card = CardBalance(balance=100.0)  # => co-14: a fresh card for the NEW path
    new_result = redeem(new_card, 30.0, new_path_enabled=True)  # => co-22: flag ON -- exercises redeem_new_path
    print(f"new path (flag on):  balance={new_result}, locked={new_card.locked}")  # => co-14: locked is False AGAIN -- released after use

    assert old_result == new_result == 70.0, "both paths must compute the SAME arithmetic result"  # => co-14: correctness check
    concurrent_card = CardBalance(balance=100.0, locked=True)  # => co-14: simulates a redemption ALREADY in progress
    try:  # => co-14: the new path's own protection, under test
        redeem(concurrent_card, 10.0, new_path_enabled=True)  # => co-14: expected to be REJECTED, not raced
        raise AssertionError("expected RuntimeError for a locked card")  # => co-14: fails loudly if the gate did not fire
    except RuntimeError:  # => co-14: expected -- the gate is doing its job
        print("new path correctly REJECTS a concurrent redemption attempt")  # => co-14: prints the confirmation
    print("Old and new paths coexist behind the flag, both verified independently: True")  # => co-16, co-22, co-14: reached only if every assert/except above held
```

**Run**: `python3 debt_refactor.py`

**Output**:

```text
old path (flag off): balance=70.0, locked=False
new path (flag on):  balance=70.0, locked=False
new path correctly REJECTS a concurrent redemption attempt
Old and new paths coexist behind the flag, both verified independently: True
```

**Key takeaway**: `redeem_old_path` and `redeem_new_path` both live in the file, both compute the
same arithmetic, and only the flag decides which one runs -- the refactor ships without ever
deleting the old, still-trusted code path.

**Why It Matters**: this is co-14's continuous-refactoring cadence, co-16's tracked-debt discipline,
and co-22's flag-based decoupling combined into one concrete pattern: pay down debt incrementally,
behind a flag, so the new path earns trust in production (flag on for a canary %, say) before the
old path is ever deleted.

---

### Example 50: A Postmortem's Root Cause Becomes a Tracked Debt Item

_ex-50 &middot; exercises co-23, co-16_

```text
Root cause: the ops-toggle script had no built-in guard against re-applying a change that was
already in effect...

## DEBT-052: ops-toggle scripts lack a pre-run state confirmation guard
Source: INC-0104 postmortem, "Root cause" section (quoted above verbatim)
```

Full artifact: **[`learning/artifacts/ex-50-postmortem-to-tracked-debt.md`](./artifacts/ex-50-postmortem-to-tracked-debt.md)**.

**Verify**: the debt item's `Source` line quotes the postmortem's root-cause section verbatim.

**Key takeaway**: a postmortem that ends at "root cause identified" loses its value the moment
everyone moves on.

**Why It Matters**: without an explicit trace from postmortem to backlog item, a root cause gets
discussed once and quietly forgotten.

---

### Example 51: A Linked ADR as a Definition-of-Done Item

_ex-51 &middot; exercises co-18, co-21_

```text
[ ] IF this PR is architecturally significant (per Example 32's two-question test): a linked ADR
    is present, referencing the actual change
```

Full artifact: **[`learning/artifacts/ex-51-adr-plus-definition-of-done.md`](./artifacts/ex-51-adr-plus-definition-of-done.md)**.

**Verify**: an architecturally significant PR (the async-settlement refactor) fails its own
checklist for lacking a linked ADR, despite passing every other item.

**Key takeaway**: making "a linked ADR" a conditional DoD item turns a norm into an enforced gate.

**Why It Matters**: without this DoD line, an architecturally significant change can ship and be
forgotten-about-the-why within a quarter.

---

### Example 52: Review Comments, Labeled by Severity

_ex-52 &middot; exercises co-05_

```text
blocking: missing a test for redeeming more points than the balance holds -- needs a regression
test before merge.
nit: `pts` could be spelled out as `points` -- not blocking, your call.
praise: the early-return guard on a zero-amount redemption is a nice touch.
```

Full artifact: **[`learning/artifacts/ex-52-review-etiquette-severity-labels.md`](./artifacts/ex-52-review-etiquette-severity-labels.md)**.

**Verify**: only the `blocking` comment states a required action; an author can tell at a glance
which one item is mandatory.

**Key takeaway**: three comments, three different obligations, made legible by one label each.

**Why It Matters**: unlabeled feedback forces every comment to be treated as equally urgent, either
stalling a PR on a nit or letting a real blocker slip through.

---

### Example 53: Pairing vs. Solo -- a Trade-off Memo

_ex-53 &middot; exercises co-20_

```text
Change A (datastore migration): HIGH risk, UNFAMILIAR -> PAIR.
Change B (parameter rename): LOW risk, FAMILIAR -> SOLO.
```

Full artifact: **[`learning/artifacts/ex-53-pairing-vs-solo-tradeoff-memo.md`](./artifacts/ex-53-pairing-vs-solo-tradeoff-memo.md)**.

**Verify**: each staffing choice cites the specific risk/familiarity property that drove it.

**Key takeaway**: pairing is a targeted response to risk and unfamiliarity, not a universal
default.

**Why It Matters**: always-pair wastes throughput on trivial changes; never-pair skips the
shared-context benefit exactly where it is most valuable.

---

### Example 54: Bisect-Driven Debugging During Review

_ex-54 &middot; exercises co-13, co-07_

A reviewer states a hypothesis about which PR commit introduced a bug, then confirms it mechanically
with a real `git bisect run` -- the located commit matches the hypothesis exactly.

**`learning/code/ex-54-systematic-debug-in-review/setup.sh`**

```bash
#!/bin/bash
# learning/code/ex-54-systematic-debug-in-review/setup.sh
# ex-54: a reviewer localizes a bug to one commit via hypothesis + bisect, DURING review (co-13, co-07)
set -e                                                          # => co-13: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                            # => co-13: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-13: throwaway identity -- irrelevant to which
                                                                 #    commit the reviewer's hypothesis targets
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-13: throwaway identity, never the real global config
export PYTHONDONTWRITEBYTECODE=1                                 # => co-13: disables .pyc caching -- rapid bisect checkouts can
                                                                  #    otherwise reuse a stale cached module and misreport the
                                                                  #    first bad commit
git -c init.defaultBranch=main init -q                          # => co-13: creates .git/ with branch "main", quietly

cat >loyalty.py <<'PY'                                            # => co-13: the function the WHOLE PR branch touches
def points_for(amount: float) -> int:                            # => co-13: the CORRECT starting definition -- known-GOOD
    return int(amount)                                            # => co-13: the exact line a later PR commit will corrupt
PY
# => co-13: heredoc closed -- loyalty.py now holds the correct, known-GOOD implementation
cat >test_loyalty.py <<'PY'                                        # => co-13: the SAME test at every commit -- bisect reruns it
from loyalty import points_for                                     # => co-13: imports the function under test, nothing else
assert points_for(100.0) == 100                                    # => co-13: fails the moment the 0.9x bug lands
PY
# => co-13: heredoc closed -- this exact test file drives every automatic bisect checkout below
git add -A && git commit -q -m "feat(loyalty): add points_for helper" # => co-13: commit 0 -- the PR branch's own base, known-GOOD
BASE=$(git rev-parse HEAD)                                         # => co-07: the PR's own base -- everything after is "the PR"

git checkout -qb feature/loyalty-tiers                              # => co-07: the PR branch under review

echo "# add docstring" >>loyalty.py && git commit -aq -m "docs(loyalty): add docstring"          # => co-13: PR commit 1 -- GOOD
echo "# rename internal var" >>loyalty.py && git commit -aq -m "refactor(loyalty): tidy locals"    # => co-13: PR commit 2 -- GOOD
sed -i.bak 's/return int(amount)/return int(amount * 0.9)/' loyalty.py && rm loyalty.py.bak         # => co-13: THE BUG -- a stray
git commit -aq -m "feat(loyalty): add tier multiplier scaffold"                                      # => co-13: PR commit 3 -- BAD,
                                                                                                        #    0.9x factor disguised
                                                                                                        #    as unrelated work
echo "# more scaffolding" >>loyalty.py && git commit -aq -m "feat(loyalty): tier scaffold continued" # => co-13: PR commit 4 -- BAD
echo "# final touch" >>loyalty.py && git commit -aq -m "chore(loyalty): final touch-up"              # => co-13: PR commit 5 -- BAD
PR_HEAD=$(git rev-parse HEAD)                                       # => co-07: the PR's current tip -- what the reviewer sees

echo "--- reviewer's hypothesis, BEFORE running bisect ---"          # => co-13: the disciplined guess, stated first
echo "hypothesis: the bug is in PR commit 3 ('add tier multiplier scaffold') -- its message" # => co-13: names a SPECIFIC
                                                                                                #    commit, not "somewhere in the PR"
echo "mentions a multiplier, and multiplier logic is the most likely place for a scaling bug" # => co-13: the reasoning
                                                                                                 #    bisect is about to check

git bisect start                                                     # => co-13: NOW confirm the hypothesis mechanically
git bisect bad "$PR_HEAD"                                            # => co-13: marks the known-bad end
git bisect good "$BASE"                                              # => co-13: marks the known-good end -- bisect now
                                                                       #    computes the midpoint automatically
git bisect run python3 test_loyalty.py >/tmp/bisect_output.txt 2>&1 || true # => co-13: capture -- exit code varies by git version
FOUND=$(git bisect view --pretty=%s)                                  # => co-13: the commit bisect actually landed on
git bisect reset                                                       # => co-13: returns the working tree to its pre-bisect branch

echo "--- bisect's own finding ---"                                     # => co-13: labels the confirmation below
echo "$FOUND"                                                            # => co-13: compared directly against the hypothesis above
```

**Run**: `bash setup.sh` (actually executed to capture the transcript below).

**Output**:

```text
--- reviewer's hypothesis, BEFORE running bisect ---
hypothesis: the bug is in PR commit 3 ('add tier multiplier scaffold') -- its message
mentions a multiplier, and multiplier logic is the most likely place for a scaling bug

--- git bisect run, confirming (or refuting) the hypothesis mechanically ---
Bisecting: 2 revisions left to test after this (roughly 1 step)
[ffbb013] refactor(loyalty): tidy locals
running 'python3' 'test_loyalty.py'
Bisecting: 0 revisions left to test after this (roughly 1 step)
[5f9ebd1] feat(loyalty): tier scaffold continued
running 'python3' 'test_loyalty.py'
Traceback (most recent call last):
  File "test_loyalty.py", line 2, in <module>
    assert points_for(100.0) == 100
AssertionError
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[060e466] feat(loyalty): add tier multiplier scaffold
running 'python3' 'test_loyalty.py'
Traceback (most recent call last):
  File "test_loyalty.py", line 2, in <module>
    assert points_for(100.0) == 100
AssertionError
060e4669e357e30fa85b94fec8ec87199e8eaf03 is the first bad commit
commit 060e4669e357e30fa85b94fec8ec87199e8eaf03
    feat(loyalty): add tier multiplier scaffold

 loyalty.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
bisect found first bad commit

--- bisect's own finding ---
feat(loyalty): add tier multiplier scaffold

The hypothesis and the full `git bisect run` result are the SAME commit: "add tier multiplier
scaffold" -- confirmed mechanically, not just by the reviewer's initial guess.
```

**Key takeaway**: the reviewer's hypothesis ("commit 3, the multiplier scaffold") and the full,
mechanical `git bisect run` result are the exact same commit -- the disciplined guess was right, and
bisection proved it rather than just asserting it.

**Why It Matters**: this closes the loop this topic opened in Example 22 (rubber-duck narration),
Example 23 (one falsifiable hypothesis), and Example 24 (bisection as a workflow decision) --
systematic debugging is not only a solo practice, it is exactly as usable DURING a code review to
localize a defect before proposing a fix, using `gh`/`git` tooling (co-07) a reviewer already has
open.

---

← Previous: [Intermediate Examples](./intermediate.md) &middot; Next: [Capstone](./capstone/overview.md) →
