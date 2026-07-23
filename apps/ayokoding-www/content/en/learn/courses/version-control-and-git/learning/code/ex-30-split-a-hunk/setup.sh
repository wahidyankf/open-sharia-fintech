#!/bin/bash
# ex-30-split-a-hunk: pressing 's' inside git add -p splits one hunk into independently-stageable pieces (co-06)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
seq 1 10 >file.txt
git add file.txt
git commit -q -m "initial 10 lines"
sed -i.bak '2s/.*/2 (edited)/' file.txt && rm -f file.txt.bak # => two edits CLOSE together (lines 2 and 9
sed -i.bak '9s/.*/9 (edited)/' file.txt && rm -f file.txt.bak #    in a 10-line file) -- close enough to
#    land in ONE hunk

printf 's\ny\nn\n' | git add -p # => "s" (split) breaks that one combined hunk into two
#    sub-hunks; then "y" stages the first sub-hunk (line 2)
#    and "n" leaves the second (line 9) unstaged

git diff --staged # => only the split-off line-2 sub-hunk is staged
git diff          # => the line-9 sub-hunk remains, entirely unstaged --
#    proof the split genuinely separated one hunk in two
