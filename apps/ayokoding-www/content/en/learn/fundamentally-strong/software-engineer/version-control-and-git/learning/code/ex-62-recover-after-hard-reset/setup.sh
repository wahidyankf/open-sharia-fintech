#!/bin/bash
# ex-62-recover-after-hard-reset: reflog + reset --hard HEAD@{1} restores commits a hard reset just discarded (co-22, co-18)
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
git log --oneline

git reset --hard HEAD~2 # => "loses" c1 and c2 -- no branch points at them
#    anymore, and `git log` can no longer see them at all
git log --oneline # => only "initial" is visible now

git reflog # => but the reflog remembers HEAD's PREVIOUS
#    position -- HEAD@{1} is exactly where HEAD sat one
#    move ago, right before this reset happened

git reset --hard 'HEAD@{1}' # => moves HEAD (and the branch, and the working
#    tree) BACK to that remembered position

git log --oneline # => c1 and c2 are back -- nothing was ever
#    actually deleted, only unreachable for a moment
