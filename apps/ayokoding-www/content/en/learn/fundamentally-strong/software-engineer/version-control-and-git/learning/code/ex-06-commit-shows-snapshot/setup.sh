#!/bin/bash
# ex-06-commit-shows-snapshot: git show prints a commit's metadata and its diff (co-07, co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add file"

git show HEAD # => "commit <hash>" / Author / Date header lines are the
#    METADATA half; everything after the blank line is a
#    normal unified diff of what this commit changed --
#    here, the whole new file appears as all-added lines
