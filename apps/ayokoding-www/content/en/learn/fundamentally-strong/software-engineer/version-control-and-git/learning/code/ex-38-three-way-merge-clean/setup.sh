#!/bin/bash
# ex-38-three-way-merge-clean: divergent, non-overlapping edits merge automatically into one commit (co-13)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "line1" >a.txt
echo "line1" >b.txt
git add . && git commit -q -m "initial"
git switch -c feature -q
echo "feature line" >>a.txt
git commit -aq -m "edit a" # => feature diverges by editing a.txt only
git switch main -q
echo "main line" >>b.txt
git commit -aq -m "edit b" # => main ALSO diverges, editing b.txt only --
#    two different files, so nothing overlaps

git merge feature -m "Merge branch 'feature'" # => both branches moved since their common ancestor,
#    so this is a genuine THREE-way merge (base + main tip
#    + feature tip) -- it succeeds automatically because
#    the two changes touch different files

git cat-file -p HEAD # => TWO "parent" lines in the raw commit object --
#    the unambiguous, low-level proof that this commit
#    really does combine two separate histories
