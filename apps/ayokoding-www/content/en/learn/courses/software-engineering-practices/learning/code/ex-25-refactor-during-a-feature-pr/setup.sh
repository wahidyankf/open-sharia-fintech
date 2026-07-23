#!/bin/bash
# learning/code/ex-25-refactor-during-a-feature-pr/setup.sh
# ex-25: a refactor folded into a feature PR, kept as its OWN separate commit (co-14, co-15)
set -e                                                          # => co-14: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-14: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-14: throwaway identity -- irrelevant to which
#    commit carries the refactor vs. the feature
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-14: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-14: creates .git/ with branch "main", quietly

cat >cart.py <<'PY' # => co-15: the pre-existing, slightly-unclear function
def calc(i, r):                                                   # => co-15: unclear parameter names -- NOT this PR's own concern
    return sum(i) * (1 - r)                                        # => co-15: the behavior this refactor must NOT change
PY
# => co-15: heredoc closed -- cart.py now holds the pre-existing, unclear-but-working function
git add cart.py && git commit -q -m "feat(cart): add calc helper" # => co-14: trunk's starting commit

git checkout -qb feature/gift-card-redemption # => co-14: the feature branch this whole example works on

sed -i.bak 's/def calc(i, r):/def calc(items: list[float], rate: float) -> float:/;
            s/return sum(i) \* (1 - r)/return sum(items) * (1 - rate)/' cart.py && rm cart.py.bak # => co-15: the REFACTOR --
#    clearer names + types, behavior UNCHANGED
git add cart.py                                                  # => co-15: staged SEPARATELY from the feature below
git commit -q -m "refactor(cart): rename calc params, add types" # => co-14, co-15: its OWN, tiny, incidental commit --
#    the boy-scout cleanup, not a separate crusade

cat >>cart.py <<'PY' # => co-14: the ACTUAL feature this PR exists to ship
def apply_gift_card(total: float, card_balance: float) -> float:    # => co-14: a NEW function -- the refactor above never
                                                                      #    touches this one at all
    return max(0.0, total - card_balance)                            # => co-14: the balance never pushes the total below $0.00
PY
# => co-14: heredoc closed -- cart.py now carries the renamed calc() AND the new gift-card function
git add cart.py                                                 # => co-14: staged separately from the refactor above
git commit -q -m "feat(cart): apply gift-card balance to total" # => co-14: the feature commit, cleanly separated

git log --oneline main..feature/gift-card-redemption # => co-14: verifies TWO distinct commits, refactor
#    then feat, not squashed into one mixed diff
