#!/bin/bash
# ex-45-rebase-abort: git rebase --abort restores the branch to its exact pre-rebase tip (co-15)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature edit" >file.txt
git commit -aq -m "feature edits line"
FEATURE_TIP_BEFORE=$(git rev-parse feature) # => remember feature's original tip hash up front
git switch main -q
echo "main edit" >file.txt
git commit -aq -m "main edits line"
git switch feature -q
git rebase main || true # => hits the same conflict ex-44 resolved

git rebase --abort # => instead of resolving, throw the WHOLE rebase
#    away -- feature returns to its state before rebase
#    ever started, no partial replay left behind

git log --oneline # => feature's history is untouched
[ "$(git rev-parse feature)" = "$FEATURE_TIP_BEFORE" ] &&
	echo "feature tip identical to pre-rebase hash: TRUE" # => the tip hash matches exactly -- proof the
#    abort was a complete, lossless rollback
git status # => clean -- no lingering rebase state at all
