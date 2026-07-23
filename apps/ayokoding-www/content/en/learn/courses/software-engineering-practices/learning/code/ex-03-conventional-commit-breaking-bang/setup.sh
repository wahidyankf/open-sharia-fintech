#!/bin/bash
# learning/code/ex-03-conventional-commit-breaking-bang/setup.sh
# ex-03: a breaking change signaled TWO independent ways -- the `!` marker and a
# `BREAKING CHANGE:` footer (co-02, co-03)
set -e                                # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR" # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-02: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-02: creates .git/ with branch "main", quietly
git commit --allow-empty -m "feat(api): add v1 endpoints" -q          # => co-02: an EARLIER commit that shipped the v1 endpoint this one removes

cat >api.py <<'PY' # => co-03: the incompatible change this commit ships
def handle_v2(request: dict) -> dict:                         # => co-03: v1's handler is GONE -- callers of v1 now fail
    return {"version": 2, **request}                           # => co-03: only the new, incompatible v2 shape remains
PY
git add api.py # => co-02: stage the one file this commit touches

git commit -m "feat(api)!: drop v1 endpoint

BREAKING CHANGE: the /v1/* routes are removed; clients must migrate to /v2/*" # => co-02: TWO independent breaking
#    signals in ONE commit -- the "!"
#    right after the scope, AND a
#    "BREAKING CHANGE:" footer

SUBJECT=$(git log -1 --pretty=%s)                                                      # => co-03: %s -- just the subject line, "!" included
BODY=$(git log -1 --pretty=%b)                                                         # => co-03: %b -- the commit body, footer included
BANG_SIGNAL=$(echo "$SUBJECT" | grep -c '!:' || true)                                  # => co-03: does the subject carry the "!" marker?
FOOTER_SIGNAL=$(echo "$BODY" | grep -c '^BREAKING CHANGE:' || true)                    # => co-03: does the body carry the footer, INDEPENDENTLY?
echo "subject: $SUBJECT"                                                               # => co-03: prints the parsed subject for inspection
echo "bang marker present: $([ "$BANG_SIGNAL" -ge 1 ] && echo true || echo false)"     # => co-03: signal 1, checked alone
echo "footer marker present: $([ "$FOOTER_SIGNAL" -ge 1 ] && echo true || echo false)" # => co-03: signal 2, checked alone
echo "either signal alone forces MAJOR: true"                                          # => co-03: SemVer's rule -- ONE of the two already suffices
