#!/bin/bash
# ex-72-checkout-remote-tracking-branch: switching to a remote-only branch name auto-creates a tracking branch (co-24)
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
git switch -c reports -q
echo "report" >report.txt
git add report.txt
git commit -q -m "add report"
git push -qu origin reports # => "reports" now exists on the
#    remote, but only ws1 has ever checked it out locally
cd "$ROOT"
git clone -q remote.git ws2 # => ws2 sees origin/reports as a
#    remote-tracking ref, but has no LOCAL reports branch
cd ws2

git switch reports # => co-24: no local branch named
#    "reports" exists yet -- Git recognizes the UNIQUE match
#    against origin/reports and creates a local tracking
#    branch from it automatically, in one command

git branch -vv # => reports now appears locally,
#    already wired to "[origin/reports]"
