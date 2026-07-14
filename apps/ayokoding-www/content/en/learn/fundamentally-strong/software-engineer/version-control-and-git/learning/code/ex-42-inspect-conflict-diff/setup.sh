#!/bin/bash
# ex-42-inspect-conflict-diff: git diff during a conflict shows a combined view of both sides (co-14)
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
git commit -aq -m "feature edits line"
git switch main -q
echo "main version" >file.txt
git commit -aq -m "main edits line"
git merge feature || true

git diff # => "diff --cc" -- Git's COMBINED diff format for an
#    unresolved conflict: a "++" prefix marks the literal
#    conflict-marker lines Git inserted, and a single "+"
#    (or "-") marks which SIDE each real content line is
#    from, all in one view instead of two separate diffs
