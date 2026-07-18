#!/bin/bash
# learning/code/ex-01-conventional-commit-fix/setup.sh
# ex-01: writing a Conventional Commits `fix` message and verifying its subject line (co-02)
set -e                                # => co-02: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR" # => co-02: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-02: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-02: creates .git/ with branch "main", quietly

echo "def parse(s): return s.strip() if s else ''" >parser.py # => co-02: the fix this commit actually ships
git add parser.py                                             # => co-02: stage the one file this commit touches

git commit -m "fix(parser): handle empty input" # => co-02: the Conventional Commits subject under test --
#    type=fix, scope=parser, description=handle empty input

git log -1 --pretty=%s # => co-02: %s prints ONLY the commit subject line -- the
#    exact string the type(scope): description grammar checks
