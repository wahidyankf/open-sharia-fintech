#!/bin/bash
# ex-49-interactive-rebase-drop: marking a commit 'drop' removes it from history entirely (co-16)
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
git commit -q -m "commit two" # => this one gets dropped below
echo "three" >three.txt
git add three.txt
git commit -q -m "commit three"

GIT_SEQUENCE_EDITOR="sed -i.bak -e '2s/^pick/drop/'" \
	GIT_EDITOR=true git rebase -i HEAD~3 # => drop skips replaying that one commit
#    entirely -- its change never lands on the rebased
#    branch at all (separate files avoid any conflict)

git log --oneline # => "commit two" is gone -- only "commit three"
#    and "commit one" remain, replayed without the middle
ls # => two.txt was never created on disk either --
#    the file that commit alone introduced never applied
