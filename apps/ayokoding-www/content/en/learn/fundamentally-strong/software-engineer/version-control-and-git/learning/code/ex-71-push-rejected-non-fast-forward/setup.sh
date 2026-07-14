#!/bin/bash
# ex-71-push-rejected-non-fast-forward: pushing an out-of-date branch is rejected, not silently overwritten (co-23)
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
git clone -q remote.git ws2 # => ws2 clones BEFORE ws1's next push
cd ws2
echo "d-change" >d.txt
git add d.txt
git commit -q -m "ws2 change"
git push -q origin main # => ws2 publishes first, advancing
#    origin/main ahead of what ws1 still has locally
cd ../ws1
echo "c-change" >c.txt
git add c.txt
git commit -q -m "ws1 change (based on the stale tip)"

git push origin main || true # => co-23: ws1's local main does
#    NOT contain ws2's commit -- pushing it would silently
#    throw that commit away, so Git REJECTS the push
#    instead ("fetch first" / non-fast-forward)
