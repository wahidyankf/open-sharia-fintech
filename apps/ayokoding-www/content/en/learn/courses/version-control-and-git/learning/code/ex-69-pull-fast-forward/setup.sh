#!/bin/bash
# ex-69-pull-fast-forward: git pull fetches then fast-forwards the local branch to match the remote (co-23, co-12)
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
git clone -q remote.git ws2
cd ws1
echo "more" >>file.txt
git commit -aq -m "second commit"
git push -q origin main
cd ../ws2

git pull # => co-23: `pull` is `fetch` PLUS an
#    integration step -- here the local main has not
#    diverged, so that integration is a plain fast-forward
#    (co-12), the same mechanism ex-36 already demonstrated

git log --oneline # => local main now shows BOTH commits
#    -- unlike plain fetch (ex-68), pull moved main itself
