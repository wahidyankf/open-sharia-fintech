#!/usr/bin/env bash
# Example 72: a 6-commit repo with TWO seeded bugs at two different commits --
# a CORRECTNESS bug (commit 3, an off-by-one) and a PERFORMANCE regression
# (commit 5, an O(n) loop replacing an O(1) multiply) -- exercising BOTH halves
# of debugging in one scenario: bisect+fix+test first, profile+fix+measure second.
set -euo pipefail # => co-09/co-10: fail fast on any error, unset variable, or failed pipe stage

git init -q                              # => co-09/co-10: a fresh, throwaway repo -- quiet mode, no default-branch chatter
git config user.email "demo@example.com" # => co-09/co-10: local commit identity, scoped to THIS repo only
git config user.name "Demo Author"       # => co-09/co-10: paired with the email above for every commit below

# co-09: commit 1 -- the correct, original O(1) implementation. The repo's
# KNOWN-GOOD starting point for the correctness bisect below.
cat >totals.py <<'PYEOF' # => co-09: writes the heredoc body below verbatim to totals.py
def line_total(price: float, qty: int) -> float:
    return price * qty
PYEOF
git add totals.py                       # => co-09: stages the new file for the first commit
git commit -q -m "commit 1: line_total" # => co-09: the KNOWN-GOOD starting point for both halves of this example

# co-09/co-04: commit 2 -- the regression test itself, added BEFORE the bug it
# will later catch (a real test-first shape: the guard exists before the fault).
cat >test_totals.py <<'PYEOF' # => co-09: writes the heredoc body below verbatim to test_totals.py
from totals import line_total


def test_line_total():
    assert line_total(2.5, 4) == 10.0
PYEOF
git add test_totals.py                           # => co-09: stages the new regression test
git commit -q -m "commit 2: add regression test" # => co-09: still correct -- the test passes here too

# co-09/co-04: commit 3 -- the SEEDED CORRECTNESS bug -- an off-by-one on qty.
# This is the TRUE first-bad commit the correctness bisect below is expected
# to land on.
cat >totals.py <<'PYEOF' # => co-09: overwrites totals.py with the off-by-one version below
def line_total(price: float, qty: int) -> float:
    # CORRECTNESS BUG: off-by-one on quantity
    return price * (qty - 1)
PYEOF
git add totals.py                                                 # => co-09: stages the seeded correctness bug
git commit -q -m "commit 3: CORRECTNESS BUG -- off-by-one on qty" # => co-09/co-04: the TRUE first-bad commit (correctness)

# co-09: commit 4 -- a distractor commit, genuinely unrelated to totals.py's
# own behavior. A correct bisect must not be fooled into blaming this one.
cat >README.md <<'READMEEOF' # => co-09: writes the heredoc body below verbatim to README.md
# totals
READMEEOF
git add README.md                                   # => co-09: stages the new, unrelated README
git commit -q -m "commit 4: add README (unrelated)" # => co-09: correctness bug still present, unchanged since commit 3

# co-09/co-13: commit 5 -- the SEEDED PERFORMANCE regression, layered ON TOP OF
# the still-unfixed correctness bug -- an O(n) accumulation loop where an O(1)
# multiply would do. This is the SECOND bug this example's later profiling
# step is expected to find and fix, independently of the correctness bug above.
cat >totals.py <<'PYEOF' # => co-13: overwrites totals.py with BOTH bugs present at once
def line_total(price: float, qty: int) -> float:
    # CORRECTNESS BUG still present (fixed later, test-first)
    # PERFORMANCE REGRESSION: pointless O(n) loop instead of O(1) multiply
    total = 0.0
    for _ in range(qty - 1):
        total += price
    return total
PYEOF
git add totals.py                                                                  # => co-13: stages the added performance regression
git commit -q -m "commit 5: PERF REGRESSION -- O(n) loop instead of O(1) multiply" # => co-09/co-13: the perf regression commit

# co-09: commit 6 -- a final distractor, appended AFTER both seeded bugs. A
# correct bisect (for either bug) must still isolate the RIGHT earlier commit.
printf '\nSee CHANGELOG.\n' >>README.md             # => co-09: appends to README.md -- totals.py itself is untouched here
git add README.md                                   # => co-09: stages the trailing README tweak
git commit -q -m "commit 6: unrelated README tweak" # => co-09: the repo's current HEAD, both bugs still present

# co-09: setup is complete -- the 6-commit history below is what a real
# `git bisect run bash check_correctness.sh` bisects through next.
echo "repo ready -- correctness bug at commit 3, perf regression at commit 5" # => confirms setup finished
git log --oneline                                                             # => co-09: shows the 6-commit history a reader is about to bisect through
