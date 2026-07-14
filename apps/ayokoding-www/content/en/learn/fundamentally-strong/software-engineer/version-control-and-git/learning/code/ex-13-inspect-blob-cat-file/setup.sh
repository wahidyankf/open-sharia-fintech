#!/bin/bash
# ex-13-inspect-blob-cat-file: git cat-file -p prints a blob's raw content by hash (co-03, co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
printf "hello\nworld\n" >file.txt
git add file.txt
git commit -q -m "add file"

git cat-file -p HEAD:file.txt # => co-03: a blob is Git's object type for raw FILE
#    CONTENT, addressed by the hash of that content --
#    HEAD:file.txt resolves "the blob file.txt pointed to
#    from HEAD's tree" and prints it byte for byte
