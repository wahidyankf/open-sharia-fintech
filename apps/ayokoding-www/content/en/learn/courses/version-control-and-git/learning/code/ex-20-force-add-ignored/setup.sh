#!/bin/bash
# ex-20-force-add-ignored: git add -f overrides .gitignore for one deliberate file (co-26)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "*.log" >.gitignore
git add .gitignore
git commit -q -m "add gitignore"
touch x.log

git add -f x.log # => -f (force) stages a file EVEN THOUGH it matches
#    an ignore pattern -- an explicit override, not a
#    permanent unignore

git status # => x.log now lists under "Changes to be committed" --
#    the single forced file is staged despite .gitignore
