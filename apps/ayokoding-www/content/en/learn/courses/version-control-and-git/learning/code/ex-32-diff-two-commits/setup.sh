#!/bin/bash
# ex-32-diff-two-commits: git diff HEAD~2 HEAD shows the combined change across two commits (co-09, co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "change one" >>file.txt
git commit -aq -m "Add change one"
echo "change two" >>file.txt
git commit -aq -m "Add change two"
echo "change three" >>file.txt
git commit -aq -m "Add change three"

git diff HEAD~2 HEAD # => co-09: diff accepts ANY two commit-ish endpoints,
#    not just working-tree/index -- this compares the tree
#    two commits back against the current tip, so BOTH
#    "change two" and "change three" appear as one diff
