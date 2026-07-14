#!/bin/bash
# ex-63-recover-deleted-branch: reflog finds a deleted branch's last tip so it can be recreated (co-22, co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c doomed -q
echo "important work" >important.txt
git add important.txt
git commit -q -m "important work on doomed branch"
DOOMED_TIP=$(git rev-parse doomed) # => note the tip hash before deleting, exactly
#    what a reader would instead read back out of reflog
git switch main -q

git branch -D doomed # => -D (force delete) removes the branch pointer
#    EVEN THOUGH its commit was never merged into main --
#    the commit itself still exists as a Git object, just
#    unreachable from any branch now
git branch # => doomed is gone from the branch list

git reflog | head -5 # => "checkout: moving from doomed to main" and
#    the commit made on doomed are both still right there
git branch recovered "$DOOMED_TIP" # => co-11: create a NEW branch pointing straight
#    at the hash reflog (or `git log -g`) revealed

git branch                  # => "recovered" now exists
git log --oneline recovered # => and its history includes "important work on
#    doomed branch" -- fully, genuinely recovered
