#!/bin/bash
# ex-46-interactive-rebase-squash: rebase -i with 'squash' folds two commits into their predecessor (co-16)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "c1" >>file.txt
git commit -aq -m "commit one"
echo "c2" >>file.txt
git commit -aq -m "commit two"
echo "c3" >>file.txt
git commit -aq -m "commit three"
git log --oneline # => three separate commits before curating

# Non-interactive stand-in for a human editing the todo list by hand: mark lines 2 and 3 "squash".
GIT_SEQUENCE_EDITOR="sed -i.bak -e '2s/^pick/squash/' -e '3s/^pick/squash/'" \
	GIT_EDITOR=true git rebase -i HEAD~3 # => co-16: squash folds "commit two" and
#    "commit three" INTO "commit one" -- one resulting
#    commit combines all three diffs and all three messages

git log --oneline      # => only ONE commit now covers what were three
git log --format=%B -1 # => the combined message concatenates all three
#    original subject lines, exactly what squash preserves
