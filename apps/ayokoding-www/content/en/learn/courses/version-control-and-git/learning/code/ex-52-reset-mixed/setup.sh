#!/bin/bash
# ex-52-reset-mixed: git reset (mixed, the default) moves HEAD and unstages, but keeps the change (co-18)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "mixed change" >>file.txt
git commit -aq -m "commit to mixed-reset"

git reset HEAD~1 # => no mode flag -- co-18: --mixed is the DEFAULT --
#    moves HEAD back AND resets the index to match, but
#    leaves the working tree's file content untouched

git log --oneline # => back to just "initial"
git status        # => the change is back, but as UNSTAGED this time
#    ("Changes not staged for commit") -- present on disk,
#    just no longer in the index the way --soft left it
