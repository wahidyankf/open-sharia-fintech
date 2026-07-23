#!/bin/bash
# ex-11-view-log-oneline: git log --oneline prints one abbreviated line per commit (co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "v1" >file.txt
git add file.txt
git commit -q -m "initial version"
echo "v2" >>file.txt
git commit -aq -m "second revision"
echo "v3" >>file.txt
git commit -aq -m "third revision"

git log --oneline # => three lines, newest first -- each line is an
#    abbreviated hash (short enough to stay unambiguous)
#    followed by that commit's subject, nothing more
