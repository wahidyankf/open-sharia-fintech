#!/bin/bash
# ex-51-reset-soft: git reset --soft moves HEAD back but leaves the change staged (co-18)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "soft change" >>file.txt
git commit -aq -m "commit to soft-reset"

git reset --soft HEAD~1 # => --soft moves ONLY HEAD (and the branch it
#    points to) back one commit -- the index and working
#    tree are left exactly as they were, completely alone

git log --oneline # => only "initial" remains in history now
git status        # => the undone commit's change reappears, already
#    STAGED -- "Changes to be committed", not unstaged
