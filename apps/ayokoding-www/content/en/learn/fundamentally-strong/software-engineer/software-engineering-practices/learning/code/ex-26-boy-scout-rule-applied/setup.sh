#!/bin/bash
# learning/code/ex-26-boy-scout-rule-applied/setup.sh
# ex-26: a tiny, incidental rename alongside an unrelated bug fix -- NOT a drive-by rewrite (co-15)
set -e                                                          # => co-15: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-15: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-15: throwaway identity -- irrelevant to how tiny
#    the eventual diff stays
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-15: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-15: creates .git/ with branch "main", quietly

cat >inventory.py <<'PY' # => co-15: a pre-existing module with ONE bad name (d)
                                                                    #    and ONE unrelated off-by-one bug (nearby)
def restock(items: list[int], d: int) -> list[int]:               # => co-15: `d` is the ONE bad name this PR incidentally fixes
    return [i + d for i in items[:-1]]                             # => co-15: `items[:-1]` is the ACTUAL bug -- drops the last item
PY
# => co-15: heredoc closed -- inventory.py now holds both the bad name AND the off-by-one bug
git add inventory.py && git commit -q -m "feat(inventory): add restock helper" # => co-15: trunk's starting commit

echo "--- while fixing an off-by-one bug, ONE nearby bad name gets renamed too ---" # => co-15: labels the sed step below
sed -i.bak \
	-e 's/def restock(items: list\[int\], d: int) -> list\[int\]:/def restock(items: list[int], delta: int) -> list[int]:/' \
	-e 's/return \[i + d for i in items\[:-1\]\]/return [i + delta for i in items]/' \
	inventory.py && rm inventory.py.bak # => co-15: `d` -> `delta` (the boy-scout cleanup, ONE
#    variable) AND items[:-1] -> items (the actual
#    off-by-one FIX) -- both tiny, in one diff

git diff --stat inventory.py # => co-15: the metric that PROVES this stayed tiny --
#    a real drive-by rewrite would show a much bigger diffstat
git add inventory.py                                                             # => co-15: stages the rename AND the fix together
git commit -q -m "fix(inventory): correct off-by-one that dropped the last item" # => co-15: the commit subject names
#    only the FIX -- the rename rides along
git log -1 --stat # => co-15: the committed diff, for the record --
#    a reviewer sees exactly one bad name renamed and
#    one off-by-one fixed, nothing broader
