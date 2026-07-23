#!/bin/bash
# kata-03-reset-hard-loses-uncommitted-work: reset --hard permanently destroys UNCOMMITTED changes -- reflog cannot help
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"

echo "=== BUGGY: muscle-memory reset --hard when meaning to just discard ONE edit ==="
echo "hours of uncommitted work" >file.txt # => never staged, never committed
git reset --hard HEAD -q                   # => --hard discards ALL uncommitted changes in the working
#    tree AND index -- there was no commit to "undo" here,
#    so this was never in the reflog to begin with
cat file.txt # => BUG: "hours of uncommitted work" is GENUINELY gone --
#    unlike Example 62's recoverable case, reflog only ever
#    remembers commits, never uncommitted working-tree edits
git reflog | head -3 # => confirms: no entry mentions the lost edit at all

echo "=== FIX: commit or stash BEFORE any --hard operation, as a safety habit ==="
echo "hours of uncommitted work, take two" >file.txt
git stash push -q -m "safety stash before risky reset" # => co-21: now genuinely recoverable
git reset --hard HEAD -q                               # => safe now -- nothing uncommitted to lose
git stash pop -q                                       # => FIXED: the work returns, because it was
#    shelved onto the stash stack BEFORE the
#    reset, not left exposed as a plain edit
cat file.txt
