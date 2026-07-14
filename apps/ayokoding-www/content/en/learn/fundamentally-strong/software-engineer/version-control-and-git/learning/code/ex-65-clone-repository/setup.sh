#!/bin/bash
# ex-65-clone-repository: git clone copies a repository's entire history into a brand-new working tree (co-01, co-23)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
mkdir source && cd source
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "more" >>file.txt
git commit -aq -m "second commit"
cd "$ROOT"

git clone source dest # => co-01/co-23: unlike `init`, clone starts
#    from an EXISTING repository -- it copies the whole
#    object database and history, then checks out a
#    working tree matching the source's default branch

test -d dest/.git && echo "dest/.git exists: TRUE" # => a genuine, independent .git/ now exists
git -C dest log --oneline                          # => -C runs the command AS IF cwd were dest
#    -- both source commits are present, full history,
#    not just the latest snapshot
