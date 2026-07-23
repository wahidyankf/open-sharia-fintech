#!/bin/bash
# kata-05-conflict-markers-committed: staging a "resolved" file without actually removing the conflict markers
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "shared line" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature version" >file.txt
git commit -aq -m "feature edits line"
git switch main -q
echo "main version" >file.txt
git commit -aq -m "main edits line"
git merge feature || true

echo "=== BUGGY: git add the conflicted file WITHOUT actually editing out the markers ==="
grep -c "<<<<<<<" file.txt || true # => confirms markers are still literally in the file
git add file.txt                   # => co-14: staging alone does NOT check content --
#    Git trusts that add means "this is resolved"
git commit --no-edit -q
grep -c "<<<<<<<" file.txt || true # => BUG: the merge commit's tree now permanently
#    contains literal <<<<<<< markers as real content

echo "=== FIX: always search for leftover markers BEFORE staging a conflict resolution ==="
cat >file.txt <<'RESOLVED'
combined: main version + feature version
RESOLVED
git add file.txt
git commit --amend --no-edit -q # => co-08: amend the just-made bad merge commit --
#    only safe because it has not been pushed yet
grep -c "<<<<<<<" file.txt || true # => FIXED: no markers anywhere in the resolved file
