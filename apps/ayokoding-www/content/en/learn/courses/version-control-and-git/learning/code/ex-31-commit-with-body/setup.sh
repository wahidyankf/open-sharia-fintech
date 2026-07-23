#!/bin/bash
# ex-31-commit-with-body: a commit can carry both a subject line and a longer explanatory body (co-07)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt

git commit -m "Add change one" -m "Explain why this change is needed in more detail
across a wrapped body paragraph." # => a second -m flag becomes the BODY, separated from
#    the subject by a blank line -- Git's own convention
#    (Chris Beams' rules) for a well-formed commit message

git log --format=%B -1 # => %B prints the RAW, full commit message -- subject,
#    blank separator line, and body all appear, confirming
#    both pieces were recorded, not just the subject
