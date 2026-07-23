#!/bin/bash
# ex-35-log-by-path: git log -- <path> restricts history to commits that touched that path (co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "c1" >>file.txt
git commit -aq -m "edit file.txt"
touch other.txt
git add other.txt
git commit -q -m "unrelated other.txt change"

git log --oneline -- file.txt # => the "unrelated other.txt change" commit is FILTERED
#    OUT entirely -- the "-- path" restriction walks the
#    history and keeps only commits whose tree actually
#    modified file.txt, in either commit
