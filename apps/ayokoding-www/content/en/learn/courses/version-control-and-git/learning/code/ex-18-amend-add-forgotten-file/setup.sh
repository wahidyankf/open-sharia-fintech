#!/bin/bash
# ex-18-amend-add-forgotten-file: --amend --no-edit folds a forgotten file into the same commit (co-08)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add feature"
echo "helper" >forgotten.txt # => a second file that SHOULD have been part of the
#    same logical change, but was left out of the commit
git add forgotten.txt

git commit --amend --no-edit # => --no-edit keeps the existing commit message as-is,
#    folding the newly staged file into the SAME commit
#    instead of creating a separate follow-up commit

git show --stat HEAD # => HEAD's tree now lists BOTH file.txt and
#    forgotten.txt -- one commit, two files, as if the
#    forgotten file had been staged the first time
