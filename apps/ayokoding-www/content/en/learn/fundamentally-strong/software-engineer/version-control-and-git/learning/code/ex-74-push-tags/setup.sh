#!/bin/bash
# ex-74-push-tags: git push --tags uploads every local tag to the remote in one call (co-25, co-23)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git
mkdir work && cd work
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "release candidate"
git remote add origin ../remote.git
git push -q origin main
git tag -a v1.0 -m "release" # => tags, like commits, start out purely LOCAL
#    -- a plain `git push` never uploads them by itself

git push origin --tags # => co-23/co-25: uploads every tag this repo
#    has that the remote lacks, in a single dedicated call

git -C ../remote.git tag # => v1.0 now genuinely exists on the "remote"
#    side too, inspected directly on the bare repository
