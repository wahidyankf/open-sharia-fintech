#!/bin/bash
# ex-26-delete-merged-branch: git branch -d removes a branch pointer once it is fully merged (co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "f1" >>file.txt
git commit -aq -m "feature work"
git switch main -q
git merge feature -q # => fast-forwards main -- feature's commit is now
#    fully reachable from main too, so nothing would be
#    lost by deleting the feature pointer

git branch -d feature # => -d (safe delete) only SUCCEEDS because Git can
#    confirm feature's commit is already merged elsewhere

git branch # => feature no longer appears -- only main remains,
#    and its history still contains the merged commit
