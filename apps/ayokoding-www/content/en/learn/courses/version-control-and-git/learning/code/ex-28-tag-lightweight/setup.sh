#!/bin/bash
# ex-28-tag-lightweight: git tag creates a lightweight, permanent pointer to one commit (co-25)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial release candidate"

git tag v1 # => a LIGHTWEIGHT tag: just a ref pointing straight
#    at HEAD's commit -- no separate tag object created,
#    unlike an annotated tag (ex-73)

git tag            # => v1 is listed among (here, the only) known tags
git rev-parse v1   # => resolves to the identical hash as...
git rev-parse HEAD # => ...HEAD itself -- v1 permanently marks this exact
#    commit, even after HEAD later moves on past it
