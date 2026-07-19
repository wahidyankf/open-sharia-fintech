#!/bin/sh
# learning/code/ex-26-small-reversible-commits/reversible_commits.sh
# ex-26-small-reversible-commits: reversible_commits.sh -- co-12
# Demonstrates driving a multi-file change as four small commits instead of
# one large diff, then reverting ONE of them independently without breaking
# the others -- the practical payoff of small, reversible steps.
set -e # => exit immediately on any command failure -- no silent partial runs

ROOT=$(mktemp -d) # => a throwaway directory, deleted by the OS eventually -- never the real repo
cd "$ROOT"        # => everything below runs inside this isolated sandbox

export GIT_AUTHOR_NAME="Demo Agent"                     # => scoped to THIS process only -- never touches any git config file
export GIT_AUTHOR_EMAIL="demo-agent@example.invalid"    # => same non-persistent scoping as GIT_AUTHOR_NAME above
export GIT_COMMITTER_NAME="Demo Agent"                  # => the committer identity, kept identical to the author here
export GIT_COMMITTER_EMAIL="demo-agent@example.invalid" # => same non-persistent scoping as GIT_COMMITTER_NAME above

git -c init.defaultBranch=main init -q # => a fresh repo, branch named "main" without touching global config

echo "module A" >a.txt                  # => step 1's payload
git add a.txt                           # => stages only step 1's file
git commit -q -m "step 1: add module A" # => small commit #1 -- one file, one concern

echo "module B" >b.txt                  # => step 2's payload
git add b.txt                           # => stages only step 2's file
git commit -q -m "step 2: add module B" # => small commit #2

echo "module C (leftover debug print)" >c.txt            # => step 3 -- deliberately the one commit worth reverting later
git add c.txt                                            # => stages only step 3's file
git commit -q -m "step 3: add module C (debug leftover)" # => small commit #3 -- isolated, so it can be undone alone

echo "module D" >d.txt                  # => step 4's payload
git add d.txt                           # => stages only step 4's file
git commit -q -m "step 4: add module D" # => small commit #4

echo "--- log before revert ---" # => a labeled section header for the captured transcript
git log --oneline                # => shows all four commits, newest first

STEP3_HASH=$(git log --oneline --grep="step 3" --format="%h") # => looks step 3's commit up BY MESSAGE, not by position
git revert --no-edit "$STEP3_HASH" >/dev/null                 # => reverts ONLY commit #3 -- #1, #2, #4 are untouched; output suppressed (timestamp varies)

echo "--- log after revert ---" # => a labeled section header for the captured transcript
git log --oneline               # => now five commits: the original four plus the revert

echo "--- files remaining on disk ---" # => a labeled section header for the captured transcript
ls -1 *.txt                            # => a.txt, b.txt, d.txt survive; c.txt is gone

test -f a.txt || {
	echo "FAIL: a.txt missing"
	exit 1
} # => step 1 must survive the revert of step 3
test -f b.txt || {
	echo "FAIL: b.txt missing"
	exit 1
} # => step 2 must survive the revert of step 3
test -f d.txt || {
	echo "FAIL: d.txt missing"
	exit 1
} # => step 4 must survive the revert of step 3
test ! -f c.txt || {
	echo "FAIL: c.txt still present"
	exit 1
} # => step 3's own file must be gone -- that's the revert's whole point

echo "Commits 1, 2, and 4 intact; commit 3 alone reverted: True" # => reached only if every check above passed
