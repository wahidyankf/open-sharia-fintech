#!/bin/bash
# ex-50-compare-merge-vs-rebase-history: the same logical integration looks different by merge vs rebase (co-17)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"

echo "=== integrate branch-a into main BY MERGE ==="
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c branch-a -q
echo "a" >>file.txt
git commit -aq -m "branch-a work"
git switch main -q
echo "m" >>main-only.txt
git add main-only.txt
git commit -q -m "main advances"
git merge --no-ff branch-a -m "Merge branch 'branch-a'" # => --no-ff so the merge commit is not silently
#    fast-forwarded away, matching a genuinely diverged case
git log --oneline --graph

echo "=== the SAME situation, integrated BY REBASE instead ==="
cd "$(mktemp -d)"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c branch-b -q
echo "b" >>file.txt
git commit -aq -m "branch-b work"
git switch main -q
echo "m" >>main-only.txt
git add main-only.txt
git commit -q -m "main advances"
git switch branch-b -q
git rebase main # => replays branch-b's one commit onto main's
#    new tip instead of merging it
git switch main -q
git merge branch-b # => now a plain fast-forward -- branch-b was
#    already rebased directly on top of main
git log --oneline --graph # => a single straight line: no merge commit,
#    no fork shape at all -- the SAME two changes, a
#    completely different-shaped history
