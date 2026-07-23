#!/bin/bash
# ex-73-annotated-tag: git tag -a creates a real tag OBJECT, not just a bare pointer (co-25)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "release candidate"

git tag -a v1.0 -m "release" # => -a (annotated) creates a genuine TAG OBJECT
#    -- unlike a lightweight tag (ex-28), this stores its
#    own message, tagger name/email, and timestamp,
#    separately from the commit it points at

git cat-file -t v1.0 # => "tag" -- a distinct object TYPE from
#    "commit", proving this is not just a plain ref
git show v1.0 # => shows the tag object's own header
#    ("Tagger:", "Date:", the -m message) FIRST, then falls
#    through to the commit it points at underneath
