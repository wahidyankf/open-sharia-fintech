#!/bin/bash
# ex-54-unstage-with-reset: git reset HEAD <path> unstages one file without touching HEAD itself (co-18, co-05)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "x" >newfile.txt
git add newfile.txt # => newfile.txt staged -- "Changes to be committed"

git reset HEAD newfile.txt # => a PATH argument narrows reset's scope down to
#    just that one file's index entry -- HEAD itself does
#    not move at all, unlike every other example on this
#    page; this is reset's oldest, path-scoped use

git status # => newfile.txt is back to "Untracked files" --
#    unstaged, with no commit undone anywhere
