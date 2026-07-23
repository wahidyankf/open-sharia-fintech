#!/bin/bash
# learning/code/ex-45-semver-changelog-from-commits/setup.sh
# ex-45: deriving a SemVer bump AND Keep a Changelog entries directly from commits since the last tag
# (co-02, co-03, co-04)
set -e                                                          # => co-04: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-04: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-04: throwaway identity -- irrelevant to the
#    derived SemVer bump or changelog content
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-04: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-04: creates .git/ with branch "main", quietly
git commit --allow-empty -q -m "chore: project scaffold"              # => co-04: pre-dates the tag -- never part of the "unreleased" window
git tag v1.4.0                                                        # => co-04: the LAST release -- everything after this is "unreleased"

git commit --allow-empty -q -m "feat(auth): add token refresh"              # => co-03: feat -> MINOR
git commit --allow-empty -q -m "fix(auth): correct token expiry off-by-one" # => co-03: fix -> PATCH
git commit --allow-empty -q -m "chore: bump ci runner image"                # => co-04: implementation-only -- EXCLUDED from the changelog
git commit --allow-empty -q -m "refactor(auth): extract token store helper" # => co-04: implementation-only -- EXCLUDED

COMMITS=$(git log --pretty=%s v1.4.0..HEAD) # => co-02: every commit subject since the last tag --
#    the ONLY input both the bump and changelog derive from

echo "--- commits since v1.4.0 ---" # => co-02: labels the raw list below
echo "$COMMITS"                     # => co-02: the raw material this whole derivation reads

HIGHEST="PATCH"                                                           # => co-03: starts at the lowest possible bump
if echo "$COMMITS" | grep -Eq '^[a-z]+(\(.+\))?!:|BREAKING CHANGE:'; then # => co-03: MAJOR beats every other signal, checked FIRST
	HIGHEST="MAJOR"                                                          # => co-03: none of the 4 commits above trigger this branch
elif echo "$COMMITS" | grep -Eq '^feat(\(.+\))?:'; then                   # => co-03: MINOR beats PATCH, checked SECOND
	HIGHEST="MINOR"                                                          # => co-03: the feat(auth) commit above DOES trigger this
fi                                                                        # => co-03: closes the if/elif opened above
echo "highest-severity commit type present -> SemVer bump: $HIGHEST"      # => co-03: the derived bump for the NEXT tag, v1.5.0 --
#    never hand-typed, always computed from commits

echo "--- derived changelog entry (feat/fix only -- chore/refactor excluded, per Example 6) ---" # => co-04: labels the heredoc below
cat <<'CHANGELOG'                                                                                # => co-04: the DERIVED changelog entry itself
## [1.5.0] - 2026-07-18

### Added

- Token refresh support, so a session no longer requires a full re-login when it expires.

### Fixed

- Corrected a token-expiry calculation that could log a user out one second early.
CHANGELOG
# => co-04: heredoc closed -- notice chore/refactor never appear above, only feat/fix made the cut
