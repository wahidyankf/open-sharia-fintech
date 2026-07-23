#!/bin/bash
# ex-14-inspect-commit-object: git cat-file -p HEAD prints a commit object's raw fields (co-03)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add file"

git cat-file -p HEAD # => a commit object is a tiny text record: "tree
#    <hash>" points at this snapshot's root directory,
#    "author"/"committer" carry who+when, and the message
#    is the last field -- no "parent" line here because
#    this is the repository's root commit
