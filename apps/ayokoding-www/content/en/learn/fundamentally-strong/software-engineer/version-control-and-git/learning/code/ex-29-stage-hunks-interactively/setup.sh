#!/bin/bash
# ex-29-stage-hunks-interactively: git add -p stages one chosen hunk, leaving the rest unstaged (co-06)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
seq 1 20 >file.txt
git add file.txt
git commit -q -m "initial 20 lines"
sed -i.bak '2s/.*/2 (edited)/' file.txt && rm -f file.txt.bak   # => two edits far apart -- far enough
sed -i.bak '19s/.*/19 (edited)/' file.txt && rm -f file.txt.bak #    that Git's default 3-line context
#    splits them into TWO hunks

printf 'y\nn\n' | git add -p # => -p walks each hunk one at a time and asks
#    y/n/q/...; "y" stages hunk 1 (the line-2 edit), "n"
#    leaves hunk 2 (the line-19 edit) alone -- one physical
#    edit session becomes two separately-stageable pieces

git diff --staged # => ONLY the line-2 hunk shows here -- it moved into
#    the index
git diff # => the line-19 hunk is still here -- still unstaged,
#    completely untouched by the first hunk's staging
