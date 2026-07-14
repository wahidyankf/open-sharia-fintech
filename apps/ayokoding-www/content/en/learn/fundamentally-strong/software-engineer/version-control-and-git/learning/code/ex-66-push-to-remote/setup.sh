#!/bin/bash
# ex-66-push-to-remote: git push origin main uploads local commits to a bare remote (co-23)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git
mkdir work && cd work
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git remote add origin ../remote.git

git push origin main # => co-23: uploads every commit main has
#    that the remote lacks, then moves the remote's own
#    "main" ref to match -- "[new branch]" because the
#    bare remote had no main ref at all before this push

git -C ../remote.git log --oneline # => the bare remote's OWN log now shows the
#    pushed commit -- proof the upload actually landed,
#    inspected directly on the "remote" side
