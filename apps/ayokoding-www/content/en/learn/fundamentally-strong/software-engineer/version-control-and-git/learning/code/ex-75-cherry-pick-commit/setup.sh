#!/bin/bash
# ex-75-cherry-pick-commit: git cherry-pick applies one specific commit's change onto another branch (co-29)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >shared.txt
git add shared.txt
git commit -q -m "initial"
git switch -c feature -q
echo "handy fix" >fix.txt
git add fix.txt
git commit -q -m "handy bugfix"
FIX_HASH=$(git rev-parse HEAD) # => the ONE commit worth taking, without
#    wanting the rest of feature's (imagined) history
git switch main -q

git cherry-pick "$FIX_HASH" # => co-29: replays JUST that commit's diff
#    onto main -- the result is a NEW commit, with a
#    different hash than the original, though the same
#    author, message, and content change

git log --oneline    # => "handy bugfix" now appears on main too
git show --stat HEAD # => and its tree genuinely contains
#    fix.txt -- a real, independent commit, not a merge
