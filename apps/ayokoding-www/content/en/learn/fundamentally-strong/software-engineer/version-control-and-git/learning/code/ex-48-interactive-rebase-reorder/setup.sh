#!/bin/bash
# ex-48-interactive-rebase-reorder: reordering lines in the rebase todo changes commit order (co-16)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >base.txt
git add base.txt
git commit -q -m "initial"
echo "one" >one.txt
git add one.txt
git commit -q -m "commit one"
echo "two" >two.txt
git add two.txt
git commit -q -m "commit two"
echo "three" >three.txt
git add three.txt
git commit -q -m "commit three" # => each commit touches its
#    OWN file, so reordering them cannot conflict
git log --oneline

# Stand-in for a human dragging line 1 below line 2 in the todo editor: swap the first two "pick" lines.
cat >swap.sh <<'HELPER'
#!/bin/bash
f="$1"
l1=$(sed -n '1p' "$f"); l2=$(sed -n '2p' "$f"); rest=$(sed -n '3,$p' "$f")
{ echo "$l2"; echo "$l1"; echo "$rest"; } > "$f"
HELPER
chmod +x swap.sh
GIT_SEQUENCE_EDITOR="$WORKDIR/swap.sh" GIT_EDITOR=true git rebase -i HEAD~3
# => co-16: the todo-list ORDER is the replay order --
#    swapping two lines swaps which commit lands first

git log --oneline # => "commit two" now precedes "commit one" -- the
#    content is identical, only the SEQUENCE changed
