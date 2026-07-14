#!/bin/bash
# ex-58-stash-changes: git stash shelves uncommitted work, leaving a clean working tree (co-21)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "half-finished work" >>file.txt # => a dirty, uncommitted, not-yet-ready edit

git stash # => pushes the current index+working-tree state
#    onto a STACK and restores the working tree to match
#    HEAD -- the edit is not lost, just set aside for now

git status # => "nothing to commit, working tree clean" --
#    as if the edit never existed, right this moment
git stash list # => exactly one entry -- the shelved change is
#    still there, just not in the working tree anymore
