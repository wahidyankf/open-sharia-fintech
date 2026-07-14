#!/bin/bash
# ex-22-switch-branch: git switch moves HEAD (and the working tree) to another branch (co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git branch feature

git switch feature # => moves HEAD to point at feature instead of main --
#    since both branches share the same commit here, the
#    working tree does not change, only which branch HEAD
#    tracks changes

git status # => "On branch feature" -- switch genuinely moved the
#    checked-out branch, confirmed by status itself
