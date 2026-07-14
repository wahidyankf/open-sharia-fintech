#!/bin/bash
# ex-59-stash-pop: git stash pop reapplies the most recent stash and removes it from the stack (co-21)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "half-finished work" >>file.txt
git stash -q

git stash pop # => reapplies stash@{0}'s changes to the
#    working tree AND drops it from the stash stack in one
#    step -- unlike `apply`, pop does not leave a copy behind

cat file.txt   # => "half-finished work" is back on disk
git stash list # => empty -- the stash was consumed by pop,
#    exactly the way the corresponding commit is consumed
#    by nothing (stashes are a stack, commits are permanent)
