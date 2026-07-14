#!/bin/bash
# ex-64-add-remote: git remote add registers a named connection to another repository (co-23)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git # => a BARE repository -- no working tree, just
#    the .git database itself; the standard shape for
#    something meant to be pushed to and fetched from,
#    used here in place of a real network host

mkdir work && cd work
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"

git remote add origin ../remote.git # => "origin" is just a LOCAL nickname for that
#    other repository's location -- a plain path here,
#    but the exact same mechanism as an ssh:// or https:// URL

git remote -v # => lists origin twice: once for fetch, once
#    for push -- they can even point at different URLs,
#    though here they are identical
