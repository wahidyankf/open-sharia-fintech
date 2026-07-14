#!/bin/bash
# ex-53-reset-hard: git reset --hard moves HEAD and overwrites the working tree to match (co-18)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "hard change" >>file.txt
git commit -aq -m "commit to hard-reset"

git reset --hard HEAD~1 # => --hard moves HEAD back AND forces the index
#    AND the working tree to match that older commit
#    exactly -- this is the DESTRUCTIVE mode of the three

git log --oneline # => back to just "initial"
git status        # => clean -- nothing left to stage or discard
cat file.txt      # => the file's content is back to "base" too --
#    the "hard change" line is genuinely gone from disk
