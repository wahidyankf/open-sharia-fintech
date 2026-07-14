#!/bin/bash
# ex-68-fetch-updates: git fetch downloads new commits without touching the local branch (co-23, co-24)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git
git clone -q remote.git ws1
cd ws1
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git push -q origin main
cd "$ROOT"
git clone -q remote.git ws2 # => a second, independent clone of the
#    same remote -- simulates a second developer's machine
cd ws1
echo "more" >>file.txt
git commit -aq -m "second commit"
git push -q origin main # => ws1 publishes a new commit
cd ../ws2

git fetch origin # => co-23/co-24: downloads the new commit
#    and updates origin/main -- but does NOT touch ws2's
#    own local main branch or its working tree at all

git log --oneline # => local main still shows just ONE
#    commit -- fetch alone never moves it
git log origin/main --oneline # => the remote-tracking ref DID
#    advance -- it now shows both commits, one step ahead
