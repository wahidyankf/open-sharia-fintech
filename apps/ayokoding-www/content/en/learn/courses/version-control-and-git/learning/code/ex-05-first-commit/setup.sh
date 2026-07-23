#!/bin/bash
# ex-05-first-commit: git commit records the staged snapshot as history (co-07)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => throwaway identity, scoped to
#    this script only -- never the developer's real config
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt

git commit -m "add file" # => moves the staged index into a new, permanent commit
# => "(root-commit)" marks it as the very first commit --
#    it has no parent, so it starts the history graph

git log --oneline # => exactly one line -- one commit exists, and only one
