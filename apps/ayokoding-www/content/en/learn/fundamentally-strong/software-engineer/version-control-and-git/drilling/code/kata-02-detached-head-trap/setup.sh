#!/bin/bash
# kata-02-detached-head-trap: committing while in detached HEAD state -- work is orphaned unless a branch is created
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "v1" >file.txt
git add file.txt
git commit -q -m "initial"
echo "v2" >>file.txt
git commit -aq -m "second commit"
FIRST=$(git rev-parse HEAD~1)

echo "=== BUGGY: checking out a commit hash directly, not a branch ==="
git checkout -q "$FIRST" # => detached HEAD -- HEAD now points straight at a commit,
#    not through any branch (co-04)
git status | head -2 # => Git itself warns about detached HEAD
echo "hotfix content" >hotfix.txt
git add hotfix.txt
git commit -q -m "hotfix work in detached HEAD"
DETACHED_TIP=$(git rev-parse HEAD)
git switch main -q # => switching branches while detached: the hotfix commit
#    has NO branch pointing at it anymore
git log --oneline | { grep -c "hotfix work" || true; } # => BUG: 0 -- the hotfix commit is unreachable
#    from main; it only survives via reflog, and only for a while

echo "=== FIX: create a branch BEFORE committing in detached HEAD, or immediately after ==="
git branch rescued "$DETACHED_TIP" # => recreates a real, permanent pointer at that commit,
#    using the hash noted before switching away (co-11)
git log --oneline rescued | { grep -c "hotfix work" || true; } # => FIXED: 1 -- reachable again, permanently, via
#    a real branch instead of a soon-to-expire reflog entry
