#!/bin/bash
# ex-34-log-limit-and-format: -N caps how many commits print, --pretty=format customizes each line (co-10)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "c1" >>file.txt
git commit -aq -m "Add change one"
echo "c2" >>file.txt
git commit -aq -m "Add change two"
echo "c3" >>file.txt
git commit -aq -m "Add change three"

git log -3 --pretty=format:"%h %s" # => -3 caps the log at the three MOST RECENT commits
#    (out of four total); --pretty=format:"%h %s" replaces
#    the default multi-line entry with one line per commit:
#    abbreviated hash (%h) then subject (%s), nothing else
