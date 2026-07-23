#!/usr/bin/env bash
# capstone-solid-core: Step 4's commit-history demo (topic 09/30 co-01..co-04). Walks this
# capstone's OWN four ordered steps as a clean Conventional-Commits history in a throwaway
# scratch repository (mktemp -d, never nested inside this content tree -- avoids an
# embedded-git-repo hazard). Each commit below copies REAL, VERBATIM excerpts from this
# capstone's shipped app/domain.py -- not invented code -- scaled down to sizes that stay fast
# and self-contained (pure stdlib + pytest, zero network installs) so EVERY commit's suite is
# genuinely run and genuinely green here, not merely asserted. Requires this capstone's own
# `.venv` (run `bash setup.sh` once from `code/` first if it does not exist yet).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ ! -x "$CODE_DIR/.venv/bin/pytest" ]; then
	echo "error: $CODE_DIR/.venv not found -- run 'bash setup.sh' from code/ first" >&2
	exit 1
fi
PYTEST="$CODE_DIR/.venv/bin/pytest"
RUFF="$CODE_DIR/.venv/bin/ruff"

WORKDIR=$(mktemp -d)
cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
git commit --allow-empty -q -m "chore: scaffold scratch repository"
git tag v1.0.0
BASE=$(git rev-parse HEAD)

echo "=== COMMIT 1/4: Step 1 -- import the Pass-1 baseline under a green test ==="
cat >streak.py <<'PY' # => VERBATIM: the O(n log n) sort-based algorithm Pass 1 shipped
from datetime import timedelta


def longest_streak_ever(checkin_dates):
    if not checkin_dates:
        return 0
    ordered = sorted(checkin_dates)
    longest = 1
    current = 1
    for previous_day, this_day in zip(ordered, ordered[1:]):
        if this_day - previous_day == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest
PY
cat >test_streak.py <<'PY'
from datetime import date

from streak import longest_streak_ever


def test_empty_history_has_no_streak():
    assert longest_streak_ever(set()) == 0


def test_three_consecutive_days_is_a_streak_of_three():
    d = date(2026, 1, 1)
    dates = {d, d.replace(day=2), d.replace(day=3)}
    assert longest_streak_ever(dates) == 3
PY
git add streak.py test_streak.py
git commit -q -m "feat(capstone): import the pass-1 longest-streak algorithm under a green test"
"$PYTEST" -q
echo "commit 1: green"

echo
echo "=== COMMIT 2/4: Step 2 -- SOLID/DIP: a repository Protocol + a fake, zero inheritance ==="
cat >ports.py <<'PY' # => distilled from the real app/ports.py's HabitRepository Protocol
from typing import Protocol


class HabitRepository(Protocol):
    def record_checkin(self, habit_id: int, checkin_date_iso: str) -> None: ...
    def checkin_dates(self, habit_id: int) -> set:  # noqa: UP006 -- kept minimal for the demo
        ...
PY
cat >test_ocp.py <<'PY' # => distilled from the real tests/test_services.py OCP proof
from datetime import date

from ports import HabitRepository
from streak import longest_streak_ever


class InMemoryHabitRepository:  # => satisfies HabitRepository by SHAPE alone, zero inheritance
    def __init__(self):
        self._by_habit = {}

    def record_checkin(self, habit_id: int, checkin_date_iso: str) -> None:
        self._by_habit.setdefault(habit_id, set()).add(date.fromisoformat(checkin_date_iso))

    def checkin_dates(self, habit_id: int) -> set:
        return self._by_habit.get(habit_id, set())


def _uses_any_habit_repository(repo: HabitRepository, habit_id: int) -> int:
    """Depends ONLY on the Protocol (topic 21 DIP) -- never on a concrete class."""
    return longest_streak_ever(repo.checkin_dates(habit_id))


def test_a_brand_new_repository_needs_zero_edits_to_existing_code():
    repo = InMemoryHabitRepository()
    repo.record_checkin(1, "2026-01-01")
    repo.record_checkin(1, "2026-01-02")
    assert _uses_any_habit_repository(repo, 1) == 2
PY
git add ports.py test_ocp.py
git commit -q -m "refactor(capstone): introduce a HabitRepository DIP port and prove OCP with a fake"
"$PYTEST" -q
echo "commit 2: green"

echo
echo "=== COMMIT 3/4: Step 3 -- O(n) algorithm, measured against the Step 1 baseline ==="
cat >streak_fast.py <<'PY' # => VERBATIM: the ordinal-based O(n) rewrite from app/domain.py
def longest_streak_ever_fast(checkin_dates):
    if not checkin_dates:
        return 0
    ordinals = {day.toordinal() for day in checkin_dates}
    longest = 0
    for ordinal in ordinals:
        if (ordinal - 1) in ordinals:
            continue
        run_length = 1
        probe = ordinal + 1
        while probe in ordinals:
            run_length += 1
            probe += 1
        longest = max(longest, run_length)
    return longest
PY
cat >test_streak_fast.py <<'PY'
import random
from datetime import date, timedelta

from streak import longest_streak_ever
from streak_fast import longest_streak_ever_fast


def _random_history(n, seed):
    rng = random.Random(seed)
    start = date(2000, 1, 1)
    return {start + timedelta(days=rng.randrange(0, n * 3)) for _ in range(n)}


def test_naive_and_fast_agree_on_twenty_random_histories():
    for seed in range(20):
        dates = _random_history(500, seed)
        assert longest_streak_ever(dates) == longest_streak_ever_fast(dates)
PY
git add streak_fast.py test_streak_fast.py
git commit -q -m "perf(capstone): replace the sort-based streak scan with an O(n) ordinal scan"
"$PYTEST" -q
echo "commit 3: green -- now measuring the real, live speedup on THIS machine:"
"$CODE_DIR/.venv/bin/python" - <<'PYEOF'
import random
import time
from datetime import date, timedelta

import sys

sys.path.insert(0, ".")
from streak import longest_streak_ever
from streak_fast import longest_streak_ever_fast

rng = random.Random(7)
start = date(2000, 1, 1)
dates = {start + timedelta(days=rng.randrange(0, 150_000)) for _ in range(50_000)}

t0 = time.perf_counter()
naive_result = longest_streak_ever(dates)
t1 = time.perf_counter()
fast_result = longest_streak_ever_fast(dates)
t2 = time.perf_counter()

assert naive_result == fast_result, "algorithms disagree -- would NOT ship this"
naive_s = t1 - t0
fast_s = t2 - t1
print(f"n=50000: naive {naive_s:.6f}s, fast {fast_s:.6f}s, {naive_s / fast_s:.2f}x")
PYEOF

echo
echo "=== COMMIT 4/4: Step 4 -- a local lint+test gate, added and proven ==="
cat >gate.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "lint:"
"$1" check .
echo "test:"
"$2" -q
SH
chmod +x gate.sh
git add gate.sh
git commit -q -m "docs(capstone): add a local lint+test gate mirroring the pipeline's own two stages"
"$RUFF" check . --quiet
bash gate.sh "$RUFF" "$PYTEST"
echo "commit 4: green"

echo
echo "=== clean history (4 commits) ==="
git log --oneline "$BASE"..HEAD

echo
echo "=== deriving the SemVer bump and changelog entry from v1.0.0..HEAD (topic 30 co-03/co-04) ==="
COMMITS=$(git log --pretty=%s v1.0.0..HEAD)
echo "$COMMITS"

HIGHEST="PATCH"
if echo "$COMMITS" | grep -Eq '^[a-z]+(\(.+\))?!:|BREAKING CHANGE:'; then
	HIGHEST="MAJOR"
elif echo "$COMMITS" | grep -Eq '^feat(\(.+\))?:'; then
	HIGHEST="MINOR"
fi
echo "highest-severity commit type present -> SemVer bump: $HIGHEST (v1.0.0 -> v1.1.0)"
