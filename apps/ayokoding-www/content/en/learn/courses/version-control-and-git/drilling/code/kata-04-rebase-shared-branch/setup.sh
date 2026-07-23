#!/bin/bash
# kata-04-rebase-shared-branch: rebasing a branch someone else already pulled breaks their next push/pull
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
echo "shared work" >>file.txt
git commit -aq -m "shared: work everyone will pull"
git push -q origin main # => this commit is now SHARED -- ws2 is about to pull it
cd "$ROOT"
git clone -q remote.git ws2 # => ws2 pulls the shared commit -- it is now relying
#    on that exact hash existing
cd ws1

echo "=== BUGGY: rebasing the ALREADY-PUSHED, already-shared commit anyway ==="
git commit --amend -q -m "shared: work everyone will pull (reworded, same effect as a rebase)"
# => co-17: amend (like rebase) gives this commit a
#    BRAND NEW hash -- the exact danger co-17 warns
#    about, applied to the simplest possible case
git push origin main || true # => BUG: rejected -- ws1's rewritten history no
#    longer contains the ORIGINAL hash the remote
#    (and ws2) still has; a normal push cannot reconcile
#    two DIFFERENT hashes claiming to be the same commit

echo "=== FIX: never rewrite a commit that has already been pushed and pulled -- add a NEW commit instead ==="
git reset --soft HEAD~1 -q                         # => co-18: undo the risky amend, keep the edit staged
git commit -q -m "shared: work everyone will pull" # => restore the ORIGINAL message/content as a
#    fresh commit on top -- do NOT reuse --amend here
echo "additional fix, as a NEW commit" >>file.txt
git commit -aq -m "fix: address feedback in a new commit, not a rewrite"
git push origin main # => FIXED: succeeds -- history only ever grew
#    forward, nothing shared was ever rewritten
