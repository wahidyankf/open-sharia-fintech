#!/bin/bash
# ex-57-restore-file-from-commit: --source=<commit> restores a file's content from any older commit (co-20)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "v1" >versioned.txt
git add versioned.txt
git commit -q -m "v1 of versioned.txt"
echo "v2" >versioned.txt
git commit -aq -m "v2 of versioned.txt"
echo "v3" >versioned.txt
git commit -aq -m "v3 of versioned.txt"
git log --oneline

git restore --source=HEAD~2 versioned.txt # => --source picks a DIFFERENT baseline than the
#    default HEAD -- HEAD~2 is two commits back, the
#    commit that introduced "v1"

cat versioned.txt # => back to "v1" -- restored from that older
#    commit's tree, with no reset or checkout of HEAD at all
git log --oneline # => still three commits -- history is completely
#    unchanged; only the working-tree FILE content moved
