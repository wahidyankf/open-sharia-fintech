#!/bin/bash
# ex-39-create-merge-conflict: overlapping edits to the same line make git merge fail with a conflict (co-14)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "shared line" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature version" >file.txt
git commit -aq -m "feature edits line" # => rewrites the SAME line
git switch main -q
echo "main version" >file.txt
git commit -aq -m "main edits line" # => main ALSO rewrites it,
#    differently -- an unavoidable overlap

git merge feature || true # => Git cannot pick a winner automatically -- it
#    reports a conflict and leaves the merge unfinished
#    rather than silently guessing which edit is "right"

git status # => "both modified: file.txt" -- Git's exact label
#    for a path both sides changed in a conflicting way
