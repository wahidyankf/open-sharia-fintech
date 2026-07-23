#!/bin/bash
# learning/code/ex-31-doc-in-same-pr-as-code/setup.sh
# ex-31: updating the README in the SAME PR that changes the behavior it documents (co-17)
set -e                                                          # => co-17: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-17: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-17: throwaway identity -- irrelevant to whether the
#    doc and code change land in the same commit
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-17: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-17: creates .git/ with branch "main", quietly

cat >README.md <<'MD' # => co-17: the docs this PR is about to make STALE
## Cart API

`apply_gift_card(total, card_balance)` -- applies a gift card balance to a cart total.
MD
# => co-17: heredoc closed -- README.md now documents the two-argument signature, about to go stale
cat >cart_api.py <<'PY' # => co-17: the code this PR is about to change
def apply_gift_card(total: float, card_balance: float) -> float:
    return max(0.0, total - card_balance)
PY
# => co-17: heredoc closed -- cart_api.py's signature EXACTLY matches what README.md just documented
git add . && git commit -q -m "feat(cart): add gift-card application" # => co-17: trunk's starting commit, doc and code in sync

git checkout -qb feature/gift-card-cap # => co-17: one PR, ONE branch, both files change together --
#    never a separate "fast-follow docs PR" after the fact
sed -i.bak 's/def apply_gift_card(total: float, card_balance: float) -> float:/def apply_gift_card(total: float, card_balance: float, max_pct: float = 1.0) -> float:/;
            s/return max(0.0, total - card_balance)/applied = min(card_balance, total * max_pct)\n    return max(0.0, total - applied)/' cart_api.py && rm cart_api.py.bak # => co-17: the BEHAVIOR change

sed -i.bak "s/\`apply_gift_card(total, card_balance)\` -- applies a gift card balance to a cart total./\`apply_gift_card(total, card_balance, max_pct=1.0)\` -- applies a gift card balance to a cart total, capped at max_pct of the total (default 100%)./" README.md && rm README.md.bak # => co-17: the DOC change, SAME commit

git add cart_api.py README.md                                                         # => co-17: both files staged together
git commit -q -m "feat(cart): cap gift-card application at a configurable percentage" # => co-17: ONE commit, both files --
#    a reviewer sees the stale-doc
#    risk resolved in the same diff

git show --stat HEAD # => co-17: proves BOTH files changed in the SAME commit --
#    a reviewer never sees code without its matching doc
