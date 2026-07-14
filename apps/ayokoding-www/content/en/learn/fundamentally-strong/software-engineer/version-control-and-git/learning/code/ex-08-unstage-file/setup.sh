#!/bin/bash
# ex-08-unstage-file: git restore --staged moves a file back out of the index (co-20, co-05)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >base.txt
git add base.txt
git commit -q -m "initial" # => a real HEAD must exist first -- restore needs a
#    baseline commit to compare the index against
echo "hello" >file.txt
git add file.txt # => file.txt is staged -- "Changes to be committed"

git restore --staged file.txt # => co-20: pulls the file back OUT of the index --
#    HEAD has no entry for file.txt, so restoring against
#    that baseline un-stages it entirely; the working-tree
#    copy on disk is left completely alone either way

git status # => file.txt returns to "Untracked files" -- unstaged,
#    but the actual edit on disk is untouched either way
