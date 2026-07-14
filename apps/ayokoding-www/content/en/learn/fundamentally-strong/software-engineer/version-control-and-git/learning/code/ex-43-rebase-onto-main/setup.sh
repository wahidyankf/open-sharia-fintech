#!/bin/bash
# ex-43-rebase-onto-main: git rebase replays a branch's commits onto a new base, new hashes, linear log (co-15)
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
git commit -aq -m "feature commit 1"
echo "f2" >>file.txt
git commit -aq -m "feature commit 2"
git switch main -q
echo "m1" >>main-only.txt
git add main-only.txt
git commit -q -m "main commit 1" # => main advanced
#    independently while feature was being developed
git switch feature -q

git rebase main # => REPLAYS each feature commit, one at a time, on
#    top of main's new tip -- every replayed commit gets a
#    brand-new hash, because its parent (and therefore its
#    own content-hash) genuinely changed

git log --oneline --graph --all # => a single straight line -- feature's two commits
#    now sit directly after main's, no fork visible at all
