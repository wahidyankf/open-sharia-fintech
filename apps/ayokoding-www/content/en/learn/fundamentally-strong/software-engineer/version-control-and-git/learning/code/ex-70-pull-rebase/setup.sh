#!/bin/bash
# ex-70-pull-rebase: git pull --rebase replays local commits atop the fetched ones instead of merging (co-24, co-15)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git
git clone -q remote.git ws1
cd ws1
echo "base" >shared.txt
git add shared.txt
git commit -q -m "initial"
git push -q origin main
cd "$ROOT"
git clone -q remote.git ws2
cd ws2
echo "local-only" >local.txt
git add local.txt
git commit -q -m "local change (own file)"
# => ws2 now has ONE commit main lacks -- it has diverged
cd ../ws1
echo "remote-only" >remote.txt
git add remote.txt
git commit -q -m "remote change (own file)"
git push -q origin main # => and origin/main ALSO advanced --
#    a genuine divergence, both sides moved independently
cd ../ws2

git pull --rebase # => co-24/co-15: fetches origin's new
#    commit, then REPLAYS ws2's own local commit on top of
#    it -- unlike a plain `pull`, this never creates a
#    merge commit, keeping history linear

git log --oneline --graph # => a straight line: the fetched
#    "remote change" commit, then the replayed "local
#    change" on top -- no fork shape anywhere
