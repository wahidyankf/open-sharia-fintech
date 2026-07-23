#!/bin/bash
# ex-23-create-and-switch: git switch -c creates and checks out a branch in one step (co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"

git switch -c hotfix # => -c COMBINES `git branch hotfix` and
#    `git switch hotfix` into a single call -- creates the
#    branch AND checks it out immediately

git branch # => hotfix exists AND is the checked-out branch ("*")
#    -- one command produced both effects at once
