#!/bin/bash
# ex-33-diff-branches: git diff main..feature shows only what feature added beyond main (co-09)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >shared.txt
git add shared.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature only" >feature.txt
git add feature.txt
git commit -q -m "feature only file"
git switch main -q

git diff main..feature # => the two-dot form diffs the TIPS of both branches
#    directly -- feature.txt appears as newly added,
#    because that is the entire delta between the two tips
