#!/bin/bash
# learning/code/ex-10-pr-size-under-100-lines/setup.sh
# ex-10: splitting one 300-line change into three right-sized PRs, each near the ~100-line bar (co-06)
set -e                                                          # => co-06: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-06: fresh, throwaway scratch repo -- deterministic, no network
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-06: throwaway identity -- irrelevant to the
#    diffstat sizes this example is actually about
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-06: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-06: creates .git/ with branch "main", quietly
git commit --allow-empty -m "chore: project scaffold" -q              # => co-06: the trunk state all three PRs branch from

gen_lines() {                                                      # => co-06: helper -- writes N numbered placeholder
	local count=$1 file=$2                                            #    lines to a file, standing in for real code so
	for i in $(seq 1 "$count"); do echo "line_$i = $i"; done >"$file" # => co-06: the diffstat below is genuine, not invented
}                                                                  # => co-06: closes the helper function opened above

git checkout -qb pr/auth-adapter                                           # => co-06: PR 1 of 3 -- auth adapter, its OWN concern
gen_lines 98 auth_adapter.py                                               # => co-06: 98 new lines -- under the ~100-line bar
git add auth_adapter.py && git commit -q -m "feat(auth): add auth adapter" # => co-06: PR 1's own commit, scoped to auth only
echo "--- PR 1: auth-adapter ---"                                          # => co-06: labels the diffstat that follows
git diff --stat main..pr/auth-adapter                                      # => co-06: the exact metric a reviewer checks size by

git checkout -q main # => co-06: back to trunk -- PR 2 branches from trunk too,
#    NOT from PR 1, so the three PRs stay independent
git checkout -qb pr/input-validation                                             # => co-06: PR 2 of 3 -- input validation, a SEPARATE concern
gen_lines 103 validation.py                                                      # => co-06: 103 new lines -- close to, slightly over, the bar
git add validation.py && git commit -q -m "feat(checkout): add input validation" # => co-06: PR 2's own commit, scoped
#    to validation only
echo "--- PR 2: input-validation ---"     # => co-06: labels the diffstat that follows
git diff --stat main..pr/input-validation # => co-06: still reviewable in one sitting despite the 103

git checkout -q main                                                                   # => co-06: back to trunk again for the third, independent PR
git checkout -qb pr/checkout-tests                                                     # => co-06: PR 3 of 3 -- regression tests, a THIRD concern
gen_lines 96 test_checkout.py                                                          # => co-06: 96 new lines -- under the ~100-line bar
git add test_checkout.py && git commit -q -m "test(checkout): add regression coverage" # => co-06: PR 3's own commit,
#    scoped to tests only
echo "--- PR 3: checkout-tests ---"     # => co-06: labels the diffstat that follows
git diff --stat main..pr/checkout-tests # => co-06: the third slice of the original 300-line change --
#    three independent, right-sized PRs instead of one
