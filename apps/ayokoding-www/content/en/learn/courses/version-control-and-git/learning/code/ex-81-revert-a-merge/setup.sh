#!/bin/bash
# ex-81-revert-a-merge: git revert -m 1 undoes a merge commit's changes without rewriting history (co-19, co-13)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature line" >>file.txt
git commit -aq -m "feature change"
git switch main -q
git merge --no-ff feature -m "Merge branch 'feature'" # => co-13: a real merge commit, two parents
MERGE_HASH=$(git rev-parse HEAD)
git log --oneline --graph

git revert -m 1 --no-edit "$MERGE_HASH" # => co-19: a merge commit has TWO
#    parents, so revert alone cannot infer which side is
#    "the" original -- -m 1 says "treat parent 1 (main) as
#    the mainline", undoing feature's contribution only

git log --oneline --graph # => the revert lands as a NEW commit
#    on top -- the merge commit and feature's own commit
#    both remain, visible in history, exactly like ex-55
cat file.txt # => back to just "base" -- the net
#    content change is undone, additively
