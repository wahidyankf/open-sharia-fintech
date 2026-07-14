#!/bin/bash
# ex-47-interactive-rebase-reword: rebase -i with 'reword' changes one commit's message, leaves others (co-16)
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

GIT_SEQUENCE_EDITOR="sed -i.bak -e '2s/^pick/reword/'" \
	GIT_EDITOR="sed -i.bak -e '1s/.*/commit two (reworded)/'" \
	git rebase -i HEAD~3 # => reword pauses to let the message of ONLY
#    "commit two" be edited -- GIT_EDITOR here stands in
#    for the human retyping the message in an editor

git log --oneline # => "commit two (reworded)" replaces the old
#    message; "commit one" and "commit three" are byte-
#    for-byte unchanged in content, though their hashes
#    still shift because a commit earlier in the chain moved
