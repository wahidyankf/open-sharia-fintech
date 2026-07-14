#!/bin/bash
# ex-27-rename-branch: git branch -m renames a branch, keeping its history intact (co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git branch old

git branch -m old new # => -m (move) renames the ref itself -- the commit it
#    points to, and that commit's whole history, is
#    completely unaffected by the rename

git branch # => "new" appears in the branch list; "old" does not
#    -- same commit, same history, only the pointer's
#    NAME changed
