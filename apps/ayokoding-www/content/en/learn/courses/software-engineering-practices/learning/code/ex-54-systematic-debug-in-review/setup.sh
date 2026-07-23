#!/bin/bash
# learning/code/ex-54-systematic-debug-in-review/setup.sh
# ex-54: a reviewer localizes a bug to one commit via hypothesis + bisect, DURING review (co-13, co-07)
set -e                                                          # => co-13: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-13: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-13: throwaway identity -- irrelevant to which
#    commit the reviewer's hypothesis targets
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-13: throwaway identity, never the real global config
export PYTHONDONTWRITEBYTECODE=1                                      # => co-13: disables .pyc caching -- rapid bisect checkouts can
#    otherwise reuse a stale cached module and misreport the
#    first bad commit
git -c init.defaultBranch=main init -q # => co-13: creates .git/ with branch "main", quietly

cat >loyalty.py <<'PY' # => co-13: the function the WHOLE PR branch touches
def points_for(amount: float) -> int:                            # => co-13: the CORRECT starting definition -- known-GOOD
    return int(amount)                                            # => co-13: the exact line a later PR commit will corrupt
PY
# => co-13: heredoc closed -- loyalty.py now holds the correct, known-GOOD implementation
cat >test_loyalty.py <<'PY' # => co-13: the SAME test at every commit -- bisect reruns it
from loyalty import points_for                                     # => co-13: imports the function under test, nothing else
assert points_for(100.0) == 100                                    # => co-13: fails the moment the 0.9x bug lands
PY
# => co-13: heredoc closed -- this exact test file drives every automatic bisect checkout below
git add -A && git commit -q -m "feat(loyalty): add points_for helper" # => co-13: commit 0 -- the PR branch's own base, known-GOOD
BASE=$(git rev-parse HEAD)                                            # => co-07: the PR's own base -- everything after is "the PR"

git checkout -qb feature/loyalty-tiers # => co-07: the PR branch under review

echo "# add docstring" >>loyalty.py && git commit -aq -m "docs(loyalty): add docstring"         # => co-13: PR commit 1 -- GOOD
echo "# rename internal var" >>loyalty.py && git commit -aq -m "refactor(loyalty): tidy locals" # => co-13: PR commit 2 -- GOOD
sed -i.bak 's/return int(amount)/return int(amount * 0.9)/' loyalty.py && rm loyalty.py.bak     # => co-13: THE BUG -- a stray
git commit -aq -m "feat(loyalty): add tier multiplier scaffold"                                 # => co-13: PR commit 3 -- BAD,
#    0.9x factor disguised
#    as unrelated work
echo "# more scaffolding" >>loyalty.py && git commit -aq -m "feat(loyalty): tier scaffold continued" # => co-13: PR commit 4 -- BAD
echo "# final touch" >>loyalty.py && git commit -aq -m "chore(loyalty): final touch-up"              # => co-13: PR commit 5 -- BAD
PR_HEAD=$(git rev-parse HEAD)                                                                        # => co-07: the PR's current tip -- what the reviewer sees

echo "--- reviewer's hypothesis, BEFORE running bisect ---"                                  # => co-13: the disciplined guess, stated first
echo "hypothesis: the bug is in PR commit 3 ('add tier multiplier scaffold') -- its message" # => co-13: names a SPECIFIC
#    commit, not "somewhere in the PR"
echo "mentions a multiplier, and multiplier logic is the most likely place for a scaling bug" # => co-13: the reasoning
#    bisect is about to check

git bisect start          # => co-13: NOW confirm the hypothesis mechanically
git bisect bad "$PR_HEAD" # => co-13: marks the known-bad end
git bisect good "$BASE"   # => co-13: marks the known-good end -- bisect now
#    computes the midpoint automatically
git bisect run python3 test_loyalty.py >/tmp/bisect_output.txt 2>&1 || true # => co-13: capture -- exit code varies by git version
FOUND=$(git bisect view --pretty=%s)                                        # => co-13: the commit bisect actually landed on
git bisect reset                                                            # => co-13: returns the working tree to its pre-bisect branch

echo "--- bisect's own finding ---" # => co-13: labels the confirmation below
echo "$FOUND"                       # => co-13: compared directly against the hypothesis above
