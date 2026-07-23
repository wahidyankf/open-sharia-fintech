#!/bin/bash
# ex-07-stage-all-changes: git add -A stages every modified/new/deleted file at once (co-05)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
printf "a\n" >alpha.txt
printf "b\n" >beta.txt
git add alpha.txt beta.txt
git commit -q -m "track alpha and beta"

echo "a2" >>alpha.txt # => modifies TWO already-tracked files independently --
echo "b2" >>beta.txt  #    neither is staged yet after these two edits

git add -A # => -A stages every change in the whole working tree in
#    one call: modified, new, AND deleted files alike

git status # => both alpha.txt and beta.txt list under "Changes to
#    be committed" -- one command staged both at once
