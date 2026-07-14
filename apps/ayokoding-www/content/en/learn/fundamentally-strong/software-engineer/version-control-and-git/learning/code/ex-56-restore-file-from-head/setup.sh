#!/bin/bash
# ex-56-restore-file-from-head: git restore discards an uncommitted edit, reverting to HEAD's version (co-20)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "committed content" >file.txt
git add file.txt
git commit -q -m "initial"
echo "accidental local edit" >>file.txt # => an UNSTAGED, uncommitted change

git restore file.txt # => co-20: with no --source, HEAD is the implicit
#    default source -- copies HEAD's version of file.txt
#    straight into the working tree, discarding the edit

cat file.txt # => back to exactly "committed content" -- the
#    accidental line is gone, with no commit involved at all
git status # => clean -- nothing left to discard or stage
