#!/bin/bash
# ex-36-fast-forward-merge: merging an undiverged branch just moves the pointer forward, no new commit (co-12)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "line1" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "line2" >>file.txt
git commit -aq -m "feature change" # => main never moved -- feature is the
#    ONLY branch with new commits, so main has not diverged
git switch main -q

git merge feature # => "Fast-forward": main's pointer simply slides up
#    to feature's tip -- no merge commit is created because
#    there was nothing on main to reconcile against

git log --oneline --graph # => a single straight line, two commits -- history
#    stays perfectly linear after a fast-forward merge
