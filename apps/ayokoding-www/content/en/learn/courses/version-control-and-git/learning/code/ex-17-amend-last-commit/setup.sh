#!/bin/bash
# ex-17-amend-last-commit: git commit --amend rewrites the tip commit with a new hash (co-08)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "iniital typo" # => deliberately misspelled subject line

git commit --amend -m "initial commit" # => REPLACES the previous commit entirely -- same
#    parent, same tree unless content also staged, but a
#    brand-new hash, because the commit's content changed

git log --oneline # => still exactly one commit, but its message and hash
#    are both the new ones -- the old commit is gone from
#    any branch, though still reachable via reflog (co-22)
