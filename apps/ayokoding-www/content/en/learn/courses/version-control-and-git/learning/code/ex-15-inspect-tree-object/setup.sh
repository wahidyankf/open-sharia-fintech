#!/bin/bash
# ex-15-inspect-tree-object: git cat-file -p 'HEAD^{tree}' lists a directory snapshot's entries (co-03)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt
mkdir sub && echo "nested" >sub/inner.txt
git add file.txt sub/inner.txt
git commit -q -m "add file and a subdirectory"

git cat-file -p 'HEAD^{tree}' # => HEAD^{tree} dereferences the commit down to its
#    root tree object -- one line per entry: file MODE,
#    object TYPE (blob for a file, tree for a directory),
#    hash, and NAME -- exactly what a directory listing
#    looks like inside Git's own object model
