#!/bin/bash
# ex-09-diff-working-tree: plain git diff compares the working tree against the index (co-09)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add file"

echo "world" >>file.txt # => an UNSTAGED edit to an already-tracked file

git diff # => shows the unstaged change: working tree vs. index --
#    "+world" is the only line the index does not have yet
