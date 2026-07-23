#!/bin/bash
# learning/code/ex-08-self-review-before-request/setup.sh
# ex-08: diffing your own branch before opening a PR catches a self-fixable issue first (co-06)
set -e                                                          # => co-06: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-06: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-06: throwaway identity -- this example's point is
#    the diff content, not who authored it
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-06: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-06: creates .git/ with branch "main", quietly
echo "def total(items): return sum(items)" >cart.py                   # => co-06: the trunk state this feature branch starts from
git add cart.py && git commit -m "feat(cart): add total helper" -q    # => co-06: trunk's starting commit, quiet

git checkout -qb feature/cart-discount # => co-06: a short-lived feature branch, off trunk
cat >>cart.py <<'PY'                   # => co-06: the new discount logic this branch adds
def apply_discount(total: float, pct: float) -> float:        # => co-06: the actual feature this branch ships
    print("DEBUG", total, pct)                                  # => co-06: a leftover debug print -- NOT meant to ship
    return total * (1 - pct)                                    # => co-06: the real discount calculation
PY
# => co-06: heredoc closed -- cart.py now carries the feature AND the stray debug print together
git add cart.py && git commit -m "feat(cart): add discount" -q # => co-06: the branch's own commit, before self-review

echo "--- diff against trunk, BEFORE self-review ---" # => co-06: labels the first diff below
git diff main..feature/cart-discount -- cart.py       # => co-06: the self-review step -- diff branch against trunk,
#    exactly as a REVIEWER would see it, before asking for one

sed -i.bak '/print("DEBUG"/d' cart.py && rm cart.py.bak             # => co-06: the self-caught fix -- remove the stray debug print
git add cart.py && git commit -m "fix(cart): remove debug print" -q # => co-06: a SEPARATE, tiny fix-up commit, self-caught
#    -- not squashed into the feature commit above

echo "--- diff against trunk, AFTER self-review ---" # => co-06: labels the second diff below
git diff main..feature/cart-discount -- cart.py      # => co-06: the same diff, now clean -- proves the issue
#    a reviewer would have flagged is already gone
