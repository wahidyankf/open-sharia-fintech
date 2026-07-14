#!/bin/bash
# ex-16-object-type: git cat-file -t reports which of the four object types a hash resolves to (co-03)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
git add file.txt
git commit -q -m "add file"

git cat-file -t HEAD # => -t asks for the TYPE only, not the content -- HEAD
#    resolves to a "commit" object, one of Git's four
#    object types (blob, tree, commit, tag)
