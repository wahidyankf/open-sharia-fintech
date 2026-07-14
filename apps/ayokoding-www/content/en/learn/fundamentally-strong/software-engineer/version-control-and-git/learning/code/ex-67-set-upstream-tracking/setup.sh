#!/bin/bash
# ex-67-set-upstream-tracking: git push -u links a local branch to its matching remote-tracking ref (co-24)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git
mkdir work && cd work
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git remote add origin ../remote.git
git push -q origin main
git switch -c feature -q
echo "f1" >>file.txt
git commit -aq -m "feature work"

git push -u origin feature # => -u (--set-upstream) does two things at
#    once: pushes feature's commit, AND records that
#    feature now TRACKS origin/feature for future push/pull

git branch -vv # => feature's line shows "[origin/feature]"
#    -- the tracking relationship co-24 describes, now
#    visible directly in the branch listing
