#!/bin/bash
# ex-61-reflog-inspect: git reflog lists every position HEAD has occupied, as HEAD@{n} entries (co-22)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "c1" >>file.txt
git commit -aq -m "c1"
echo "c2" >>file.txt
git commit -aq -m "c2"
echo "c3" >>file.txt
git commit -aq -m "c3"

git reflog # => co-22: a LOCAL, per-repo log of every move HEAD
#    has made -- each entry is HEAD@{n} (n=0 is the most
#    recent), the hash it pointed to, and WHY it moved
#    ("commit", "checkout", "reset", ...) -- this exists
#    independently of the commit graph itself
