#!/bin/bash
# kata-08-cherry-pick-then-merge-duplicate: cherry-picking a commit, then later merging its source branch,
# leaves the fix's CONTENT duplicated across two different commit hashes in permanent history
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >shared.txt
git add shared.txt
git commit -q -m "initial"
git switch -c feature -q
echo "urgent fix" >fix.txt
git add fix.txt
git commit -q -m "urgent bugfix needed on main now"
FIX_HASH=$(git rev-parse HEAD)
echo "later feature work" >more.txt
git add more.txt
git commit -q -m "unrelated feature work"
git switch main -q
echo "main also advances" >>shared.txt
git commit -aq -m "main: unrelated progress" # => main diverges
#    BEFORE the cherry-pick, so the cherry-picked
#    commit gets a genuinely different parent (and
#    therefore a different hash) than the original

echo "=== RISKY: cherry-pick the urgent fix onto main immediately (co-29) ==="
git cherry-pick "$FIX_HASH" >/dev/null # => main gets the fix NOW, without waiting for
#    the rest of feature's (unrelated) work
git log --oneline

echo "=== LATER: feature is fully done and gets merged normally ==="
git merge --no-ff feature -m "Merge branch 'feature'" -q
git log --oneline --graph # => "urgent bugfix" now appears TWICE in
#    history -- once as the cherry-picked commit
#    (a DIFFERENT hash, replayed onto main's later
#    tip), once again as feature's own original
#    commit, reachable through the merge's second parent

echo "=== WHY THIS IS SAFE, NOT A CONFLICT: Git's merge machinery still gets it right ==="
git diff main~1 main -- fix.txt # => empty -- the merge itself introduces NO
#    further change to fix.txt; its content was
#    already identical on both sides, so the merged
#    tree is correct either way, just with two
#    commit objects recording the same change instead of one
