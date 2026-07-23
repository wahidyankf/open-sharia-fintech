#!/bin/bash
# ex-25-list-refs: git show-ref lists every ref and the commit hash it points to (co-04)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git branch feature
git branch hotfix

git show-ref # => one line per ref: the full hash it currently
#    resolves to, then the ref's full name -- confirms
#    every branch really is "just a named pointer" (co-04)
git branch -v # => the more readable branch-scoped equivalent: each
#    branch name, its ABBREVIATED hash, and its subject
