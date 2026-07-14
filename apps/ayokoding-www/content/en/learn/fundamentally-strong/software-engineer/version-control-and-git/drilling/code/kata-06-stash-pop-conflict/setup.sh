#!/bin/bash
# kata-06-stash-pop-conflict: popping a stash after the working tree has ALSO changed the same lines
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "stashed edit" >>file.txt
git stash push -q -m "wip: half-done feature" # => shelves the edit, working tree returns to "base"

echo "=== BUGGY: forgetting a stash exists, making an UNRELATED edit to the same file, then popping ==="
echo "a different, newer edit" >>file.txt # => a genuinely new edit, made without remembering
#    the earlier stash existed
git stash pop || true # => BUG: CONFLICT -- both the stash's shelved
#    line and the new edit try to occupy the same spot
git status | head -4

echo "=== FIX: git stash list BEFORE editing, or resolve the conflict like any other (co-14) ==="
sed -i.bak '/<<<<<<<\|=======\|>>>>>>>/d' file.txt && rm -f file.txt.bak # => remove markers, keep both real lines
cat file.txt
git add file.txt
git stash drop -q # => FIXED: conflict resolved by hand, exactly
#    like a merge conflict; the stash entry
#    itself (already merged in) is now redundant
git stash list # => empty -- nothing left shelved
