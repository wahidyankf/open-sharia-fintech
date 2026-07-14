#!/bin/bash
# ex-41-abort-merge: git merge --abort cleanly cancels a conflicted merge in progress (co-14)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "shared line" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature version" >file.txt
git commit -aq -m "feature edits line"
git switch main -q
echo "main version" >file.txt
git commit -aq -m "main edits line"
git merge feature || true # => stuck mid-conflict, file.txt full of markers

git merge --abort # => throws the whole in-progress merge away --
#    restores both the index AND the working tree to
#    exactly how they looked right before `git merge` ran

git status # => "nothing to commit, working tree clean" -- as if
#    the merge attempt had never happened at all
