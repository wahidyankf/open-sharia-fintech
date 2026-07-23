#!/bin/bash
# learning/capstone/code/tdd-and-history.sh
# Capstone Steps 1-2: TDD a feature (RED -> GREEN -> REFACTOR, a prerequisite skill from topic 15,
# Software Testing -- this topic does not re-teach TDD mechanics), then craft a clean
# conventional-commit history from the messy WIP sequence that real TDD work naturally produces
# (co-01, co-02), then derive the SemVer bump and changelog entry the clean history implies
# (co-03, co-04).
set -e                                # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR" # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q                   # => co-02: creates .git/ with branch "main", quietly
git commit --allow-empty -q -m "chore: project scaffold" # => co-01: trunk's starting point -- the feature branch's base
git tag v1.0.0                                           # => co-03: the LAST release -- everything after this is "unreleased"
BASE=$(git rev-parse HEAD)                               # => co-01: remembers exactly where the branch forked from

git checkout -qb feature/points-redemption-cap # => co-01: a SHORT-LIVED feature branch, off trunk

echo "=== STEP 1a: RED -- a failing test against a not-yet-implemented stub ===" # => labels the RED phase below
cat >redemption.py <<'PY'                                                        # => the stub -- exists so the import succeeds, but does nothing yet
def redeem_points(cart_subtotal, points_requested):
    raise NotImplementedError
PY
cat >test_redemption.py <<'PY' # => the test written BEFORE the real implementation
from redemption import redeem_points

def test_redeem_within_cap_succeeds():
    assert redeem_points(cart_subtotal=100.0, points_requested=40.0) == 40.0

def test_redeem_above_cap_raises():
    import pytest
    with pytest.raises(ValueError):
        redeem_points(cart_subtotal=100.0, points_requested=60.0)
PY
git add redemption.py test_redemption.py # => a WIP commit -- not yet the clean history Step 2 produces
git commit -q -m "wip: add test file and stub"
python3 -m pytest -q test_redemption.py || true # => EXPECTED to fail -- confirms the test can fail before it can pass

echo                                                                    # => blank line for readability
echo "=== STEP 1b: GREEN -- the minimal implementation that passes ===" # => labels the GREEN phase below
cat >redemption.py <<'PY'                                               # => just enough logic to satisfy both tests, nothing more
def redeem_points(cart_subtotal, points_requested):
    if points_requested > cart_subtotal * 0.5:
        raise ValueError("over cap")
    return points_requested
PY
git add redemption.py # => a SECOND WIP commit
git commit -q -m "wip: make it pass"
python3 -m pytest -q test_redemption.py # => EXPECTED to pass -- both tests are now satisfied

echo                                                                               # => blank line for readability
echo "=== STEP 1c: REFACTOR -- types, a named constant, ruff-clean formatting ===" # => labels the REFACTOR phase below
cat >redemption.py <<'PY'                                                          # => the SAME behavior, now with DD-39 type annotations and a named business rule
from __future__ import annotations

MAX_REDEMPTION_FRACTION = 0.5


def redeem_points(cart_subtotal: float, points_requested: float) -> float:
    if points_requested > cart_subtotal * MAX_REDEMPTION_FRACTION:
        raise ValueError(
            f"points_requested={points_requested} exceeds the "
            f"{MAX_REDEMPTION_FRACTION:.0%} cap of cart_subtotal={cart_subtotal}"
        )
    return points_requested
PY
ruff format --quiet redemption.py test_redemption.py # => co-10: the SAME formatter a pre-commit hook would run
git add redemption.py                                # => a THIRD WIP commit -- still messy, still on this branch
git commit -q -m "wip: refactor with types"
python3 -m pytest -q test_redemption.py     # => EXPECTED to pass -- refactoring must not change behavior
ruff check redemption.py test_redemption.py # => co-09: the lint gate, run locally BEFORE it ever reaches CI

echo                                                    # => blank line for readability
echo "=== messy history BEFORE cleanup (3 commits) ===" # => labels the first log below
git log --oneline "$BASE"..HEAD                         # => three non-conventional "wip:" subjects -- accurate but low-signal

echo                                                                      # => blank line for readability
echo "=== STEP 2: collapse into a clean, conventional-commit history ===" # => labels the cleanup below
git reset --mixed "$BASE"                                                 # => co-02: resets HEAD and the index, but keeps the working tree's FINAL content
git add test_redemption.py                                                # => co-02: the FIRST clean commit's own scope -- the test, alone
git commit -q -m "test(loyalty): add failing test for capped points redemption"
git add redemption.py # => co-02: the SECOND clean commit's own scope -- the implementation, alone
git commit -q -m "feat(loyalty): cap points redemption at 50 percent of cart subtotal"

echo "=== clean history AFTER cleanup (2 commits) ===" # => labels the second log below
git log --oneline "$BASE"..HEAD                        # => two correctly typed and scoped commits -- SAME final content as the messy version
echo "TEST_SHA=$(git log -1 --format=%h HEAD~1)"       # => the test commit's own short hash, referenced by adr-0001.md
echo "FEAT_SHA=$(git log -1 --format=%h HEAD)"         # => the feat commit's own short hash, referenced by adr-0001.md

echo                                                                          # => blank line for readability
echo "=== deriving the SemVer bump and changelog entry from v1.0.0..HEAD ===" # => labels the derivation below
COMMITS=$(git log --pretty=%s v1.0.0..HEAD)                                   # => co-04: every commit subject since the last tag -- the raw material for both derivations
echo "$COMMITS"                                                               # => co-04: shown so the derivation below is checkable against the raw list

HIGHEST="PATCH"                                                           # => co-03: starts at the lowest possible bump
if echo "$COMMITS" | grep -Eq '^[a-z]+(\(.+\))?!:|BREAKING CHANGE:'; then # => co-03: MAJOR beats every other signal, checked FIRST
	HIGHEST="MAJOR"
elif echo "$COMMITS" | grep -Eq '^feat(\(.+\))?:'; then # => co-03: MINOR beats PATCH, checked SECOND
	HIGHEST="MINOR"
fi                                                                                      # => co-03: closes the if/elif opened above
echo "highest-severity commit type present -> SemVer bump: $HIGHEST (v1.0.0 -> v1.1.0)" # => co-03: the derived bump -- test(...) commits carry no release-facing meaning, only feat/fix/! do

echo "--- derived changelog entry (test-only commits excluded, per Example 6) ---" # => co-04: labels the heredoc below
cat <<'CHANGELOG'                                                                  # => co-04: the DERIVED changelog entry itself
## [1.1.0] - 2026-07-18

### Added

- A single points redemption is now capped at 50% of the cart subtotal, closing a fraud-detection
  gap where a compromised account's points could zero out an entire order in one transaction.
CHANGELOG
