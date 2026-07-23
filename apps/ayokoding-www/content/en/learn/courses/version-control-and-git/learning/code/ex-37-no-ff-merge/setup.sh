#!/bin/bash
# ex-37-no-ff-merge: --no-ff forces a real merge commit even when a fast-forward was possible (co-13)
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
git commit -aq -m "feature change"
git switch main -q

git merge --no-ff feature -m "Merge branch 'feature'" # => --no-ff REFUSES the fast-forward shortcut on
#    purpose -- it creates a genuine merge commit with two
#    parents even though main could have just slid forward

git log --oneline --graph # => the "*   " / "|\" / "| *" / "|/" shape is a real
#    fork-and-rejoin -- feature's own commit stays visible
#    as a distinct point in history, not silently absorbed
