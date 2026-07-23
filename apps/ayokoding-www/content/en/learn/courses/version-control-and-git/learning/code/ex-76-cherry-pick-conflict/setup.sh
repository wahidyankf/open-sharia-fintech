#!/bin/bash
# ex-76-cherry-pick-conflict: resolving a cherry-pick conflict then --continue finishes applying the commit (co-29, co-14)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "line" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature edit" >file.txt
git commit -aq -m "feature edits line"
FIX_HASH=$(git rev-parse HEAD)
git switch main -q
echo "main edit" >file.txt
git commit -aq -m "main edits line first" # => main independently rewrote
#    the SAME line cherry-pick is about to touch

git cherry-pick "$FIX_HASH" || true # => the replay conflicts, exactly
#    like a merge or rebase conflict would (co-14)
git status # => "currently cherry-picking"

echo "resolved: combined edit" >file.txt # => the human resolution
git add file.txt
git cherry-pick --continue --no-edit # => finishes applying the
#    cherry-picked commit now that the conflict is resolved

git log --oneline # => the cherry-picked change
#    lands as a real commit on main, conflict and all
