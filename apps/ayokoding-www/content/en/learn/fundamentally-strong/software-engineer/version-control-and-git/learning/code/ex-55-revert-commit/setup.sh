#!/bin/bash
# ex-55-revert-commit: git revert adds a new inverse commit, undoing a change without rewriting history (co-19)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "line1" >file.txt
git add file.txt
git commit -q -m "initial"
echo "line2 (buggy)" >>file.txt
git commit -aq -m "buggy change"

git revert --no-edit HEAD # => co-19: creates a BRAND NEW commit whose diff is
#    the exact inverse of "buggy change" -- the ORIGINAL
#    commit still exists in history, untouched, unlike reset

git log --oneline # => THREE commits now: initial, buggy change, AND
#    the revert -- nothing was erased, only added to
cat file.txt # => the file's content is back to just "line1" --
#    the net effect matches reset --hard, the history does not
