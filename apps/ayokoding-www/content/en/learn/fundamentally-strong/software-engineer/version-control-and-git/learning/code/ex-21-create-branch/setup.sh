#!/bin/bash
# ex-21-create-branch: git branch <name> creates a new pointer without switching to it (co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"

git branch feature # => creates a new branch pointer at the CURRENT
#    commit -- cheap, instant, and does NOT check it out;
#    the working tree stays on main throughout

git branch # => lists both branches -- "*" marks the checked-out
#    one (main); feature exists but is not active yet
