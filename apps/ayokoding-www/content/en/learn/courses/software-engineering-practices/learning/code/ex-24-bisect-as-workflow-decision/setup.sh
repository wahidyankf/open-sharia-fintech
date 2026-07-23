#!/bin/bash
# learning/code/ex-24-bisect-as-workflow-decision/setup.sh
# ex-24: choosing bisection over a linear scan across 40 candidate commits (co-13)
set -e                                                                # => co-13: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                                 # => co-13: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"       # => co-13: throwaway identity -- irrelevant to the bisect search
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-13: throwaway identity, never the real global config
export PYTHONDONTWRITEBYTECODE=1                                      # => co-13: disables .pyc caching -- rapid bisect checkouts can
#    otherwise reuse a stale cached module and misreport the
#    first bad commit
git -c init.defaultBranch=main init -q # => co-13: creates .git/ with branch "main", quietly

cat >parity.py <<'PY' # => co-13: the function this whole regression lives in
def is_even(n: int) -> bool:                                      # => co-13: the CORRECT starting definition -- known-GOOD
    return n % 2 == 0                                              # => co-13: the exact line the bug later flips
PY
# => co-13: heredoc closed -- parity.py now holds the correct, known-GOOD implementation
git add parity.py && git commit -q -m "feat(parity): add is_even" # => co-13: commit 1 of 40 -- known-GOOD, tagged below

cat >test_parity.py <<'PY' # => co-13: the SAME test at every one of the 40 commits --
from parity import is_even                                          # => co-13: `git bisect run` reruns this unchanged each step
assert is_even(4) is True                                           # => co-13: positive case -- must hold at every GOOD commit
assert is_even(7) is False                                          # => co-13: negative case -- flips to True once the bug lands
PY
# => co-13: heredoc closed -- this exact test file drives every automatic bisect checkout below
git add test_parity.py && git commit -q -m "test(parity): add regression test" # => co-13: commit 2 of 40 -- still known-GOOD
GOOD_COMMIT=$(git rev-parse HEAD)                                              # => co-13: this is the known-GOOD end of the range --
#    `git bisect good` below anchors the search here

for i in $( # => co-13: 26 unrelated, GOOD commits -- noise around the bug
	seq 1 26
); do
	echo "# unrelated change $i" >>parity.py       # => co-13: a harmless append, never touches is_even's logic
	git commit -aq -m "chore: unrelated change $i" # => co-13: one of the 26 GOOD commits before the bug lands
done                                            # => co-13: closes the loop opened above

sed -i.bak 's/n % 2 == 0/n % 2 == 1/' parity.py && rm parity.py.bak # => co-13: THE BUG -- flips even/odd, introduced HERE
git commit -aq -m "refactor(parity): tidy modulo expression"        # => co-13: commit ~28 of 40 -- the FIRST bad commit,
#    disguised as an innocuous refactor

for i in $( # => co-13: 13 more commits AFTER the bug, still all bad
	seq 27 39
); do
	echo "# unrelated change $i" >>parity.py       # => co-13: another harmless append, bug already landed
	git commit -aq -m "chore: unrelated change $i" # => co-13: one of the 13 BAD commits, noise around the bug
done                                            # => co-13: closes the loop opened above -- 40 commits total
BAD_COMMIT=$(git rev-parse HEAD)                # => co-13: this is the known-BAD end of the range --
#    `git bisect bad` below anchors the search here

echo "total commits: $(git rev-list --count HEAD)"                                # => co-13: confirms all 40 exist
echo "log2(40) ~= 5.3, so bisection needs ~6 steps vs up to 40 for a linear scan" # => co-13: the justification itself

git bisect start               # => co-13: begins the bisection session
git bisect bad "$BAD_COMMIT"   # => co-13: marks the known-bad end
git bisect good "$GOOD_COMMIT" # => co-13: marks the known-good end -- bisect now
#    computes the midpoint automatically
git bisect run python3 test_parity.py # => co-13: `run` scripts the whole search -- exit 0=good,
#    1-127(except 125)=bad, per each step's automatic checkout
git bisect log   # => co-13: the full trail of steps bisect actually took
git bisect reset # => co-13: returns the working tree to its pre-bisect branch
