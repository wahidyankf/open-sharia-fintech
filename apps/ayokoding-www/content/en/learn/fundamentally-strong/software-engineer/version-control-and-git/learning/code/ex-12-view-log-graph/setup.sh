#!/bin/bash
# ex-12-view-log-graph: git log --graph draws the commit history as ASCII art (co-10)
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
git commit -aq -m "feature work" # => feature now has one commit main lacks

git log --graph --oneline --all # => --all shows EVERY branch's history, not just the
#    checked-out one; the "*" and "|" characters draw the
#    fork where feature diverged from main visually
