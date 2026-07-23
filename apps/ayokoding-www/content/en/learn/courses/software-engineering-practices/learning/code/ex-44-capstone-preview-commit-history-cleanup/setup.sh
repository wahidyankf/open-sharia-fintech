#!/bin/bash
# learning/code/ex-44-capstone-preview-commit-history-cleanup/setup.sh
# ex-44: rewriting a messy 8-commit branch into a clean conventional-commit history (co-02, co-01)
set -e                                                          # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-02: throwaway identity -- irrelevant to which
#    commits get squashed and rewritten below
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-02: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-02: creates .git/ with branch "main", quietly
git commit --allow-empty -m "chore: project scaffold" -q              # => co-01: trunk's starting point -- the feature branch's base
BASE=$(git rev-parse HEAD)                                            # => co-01: remembers exactly where the branch forked from

git checkout -qb feature/loyalty-points # => co-01: a SHORT-LIVED feature branch, off trunk

echo "def points(x): pass" >loyalty.py && git add -A && git commit -q -m "wip"                               # => co-02: messy commit 1 of 8
echo "def points(x): return x" >>loyalty.py && git add -A && git commit -q -m "more wip"                     # => co-02: messy commit 2 of 8
echo "# fix typo" >>loyalty.py && git add -A && git commit -q -m "fix typo"                                  # => co-02: messy commit 3 of 8
echo "def redeem(x): pass" >>loyalty.py && git add -A && git commit -q -m "oops forgot this"                 # => co-02: messy commit 4 of 8
echo "wip2" >>loyalty.py && git add -A && git commit -q -m "asdf"                                            # => co-02: messy commit 5 of 8
echo "def test_points(): assert points(10) == 10" >test_loyalty.py && git add -A && git commit -q -m "tests" # => co-02: messy commit 6
echo "# cleanup" >>loyalty.py && git add -A && git commit -q -m "cleanup"                                    # => co-02: messy commit 7 of 8
echo "def redeem(x): return max(0, x)" >loyalty_redeem_fix.py && git add -A && git commit -q -m "wip3"       # => co-02: messy commit 8 of 8

echo "--- messy history, BEFORE cleanup (8 commits) ---" # => co-02: labels the first log below
git log --oneline "$BASE"..HEAD                          # => co-02: eight non-conventional, low-signal subjects

git reset --mixed "$BASE" # => co-02: collapses all 8 commits' CONTENT back to the
#    working tree, UNSTAGED -- history reset, files kept
git add loyalty.py                                                      # => co-02: the FIRST clean commit's own scope -- feature only
git commit -q -m "feat(loyalty): add points calculation and redemption" # => co-01: one commit, one logical change -- unlike
#    the 8 messy commits it replaces
git add test_loyalty.py loyalty_redeem_fix.py                            # => co-02: the SECOND clean commit's own scope -- tests only
git commit -q -m "test(loyalty): add points calculation regression test" # => co-01: a SEPARATE commit for tests, not folded
#    into the feature commit above

echo "--- clean history, AFTER cleanup (2 commits) ---" # => co-02: labels the second log below
git log --oneline "$BASE"..HEAD                         # => co-02: verifies each commit is correctly typed and scoped
