#!/bin/bash
# kata-07-forgot-push-tags: a tag exists locally but was never pushed, so nobody else can see the release
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

echo "=== BUGGY: tag the release, push main, but forget --tags ==="
git tag -a v1.0 -m "release"
git push -q origin main  # => a plain push NEVER includes tags (co-25)
git -C ../remote.git tag # => BUG: empty -- the remote has no tags at all,
#    even though main itself is fully up to date

echo "=== FIX: git push --tags (or push the specific tag by name) ==="
git push origin --tags   # => FIXED: uploads every local tag the remote lacks
git -C ../remote.git tag # => v1.0 now genuinely exists on the remote
