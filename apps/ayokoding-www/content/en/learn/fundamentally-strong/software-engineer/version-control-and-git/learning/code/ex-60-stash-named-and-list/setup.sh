#!/bin/bash
# ex-60-stash-named-and-list: git stash push -m attaches a human-readable label to a stash entry (co-21)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "wip edit" >>file.txt

git stash push -m "wip: half-done feature" # => `push` is the modern, explicit spelling of
#    plain `git stash`; -m attaches a MESSAGE so the stash
#    is identifiable later instead of just "WIP on main: ..."

git stash list # => the labeled entry shows the custom message
#    verbatim, not the generic auto-generated description
