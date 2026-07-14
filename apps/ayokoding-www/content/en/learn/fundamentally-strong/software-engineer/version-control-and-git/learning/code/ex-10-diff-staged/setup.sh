#!/bin/bash
# ex-10-diff-staged: git diff --staged compares the index against HEAD (co-09, co-02)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add file"
echo "world" >>file.txt
git add file.txt # => the edit is now staged -- index differs from HEAD,
#    but working tree now EQUALS the index (nothing left
#    unstaged)

git diff --staged # => shows index vs. HEAD: the same "+world" line, but
#    from a different comparison than plain `git diff`

git diff # => plain diff is now EMPTY -- working tree matches the
#    index exactly, so there is nothing left to compare
