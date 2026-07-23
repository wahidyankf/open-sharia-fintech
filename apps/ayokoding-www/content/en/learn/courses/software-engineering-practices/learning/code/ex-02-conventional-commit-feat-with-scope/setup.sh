#!/bin/bash
# learning/code/ex-02-conventional-commit-feat-with-scope/setup.sh
# ex-02: a scoped `feat` commit and the MINOR bump it implies under SemVer (co-02, co-03)
set -e                                                          # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-02: throwaway author identity -- irrelevant to the
#    SemVer derivation below; only the commit TYPE prefix matters
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-02: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-02: creates .git/ with branch "main", quietly
git commit --allow-empty -m "chore: project scaffold" -q              # => co-02: an unrelated PRIOR commit -- this example's
#    subject is the SECOND commit, not the repo's first

cat >auth.py <<'PY' # => co-03: the additive capability this feat commit ships
def refresh_token(old: str) -> str:                         # => co-03: a NEW public function -- callers GAIN a capability
    return f"refreshed-{old}"                                # => co-03: existing callers of the module are untouched
PY
# => co-03: heredoc closed -- auth.py now holds exactly this one new function, nothing else changed
git add auth.py # => co-02: stage the one file this commit touches

git commit -m "feat(auth): add token refresh" # => co-02: type=feat, scope=auth, description=add token refresh

TYPE=$(git log -1 --pretty=%s | sed -E 's/^([a-z]+)(\(.*\))?!?:.*/\1/') # => co-03: parse the TYPE prefix back out of %s --
#    strips any (scope) and the trailing colon,
#    leaving only the bare type word
case "$TYPE" in                                 # => co-03: SemVer's own type-to-bump mapping, applied mechanically
feat) BUMP="MINOR" ;;                           # => co-03: feat = a new, backward-compatible capability
fix) BUMP="PATCH" ;;                            # => co-03: fix = a backward-compatible bug fix
*) BUMP="NONE" ;;                               # => co-03: any other type implies no version bump alone
esac                                            # => co-03: closes the case statement opened above
echo "commit type: $TYPE -> SemVer bump: $BUMP" # => co-03: prints the derived mapping -- TYPE=feat here,
#    so BUMP resolves to MINOR, matching this file's header
