#!/bin/bash
# ex-40-resolve-conflict: removing conflict markers and committing finishes an interrupted merge (co-14)
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
git merge feature || true # => leaves file.txt full of <<<<<<</=======/>>>>>>>
#    conflict markers around BOTH candidate versions

echo "combined: main version + feature version" >file.txt # => the human decision: replace the markers
#    with the actually-intended resolved content
git add file.txt     # => re-staging tells Git "this path is resolved now"
git commit --no-edit # => with no message override, Git reuses its own
#    auto-generated "Merge branch 'feature'" message

git log --graph --oneline # => the merge commit appears in the graph, exactly
#    like a conflict-free merge -- the resolution is
#    invisible in the graph shape, only in the tree content
