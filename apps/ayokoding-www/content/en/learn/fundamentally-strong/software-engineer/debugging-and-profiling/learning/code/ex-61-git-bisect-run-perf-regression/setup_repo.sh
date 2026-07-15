#!/usr/bin/env bash
# Example 61: a 6-commit repo where commit 4 introduces a real PERFORMANCE
# regression (an accidental O(n^2) algorithm swapped in for an O(n) one) --
# check.sh fails when a benchmark run exceeds a fixed millisecond threshold.
set -euo pipefail # => co-10: fail fast on any error, unset variable, or failed pipe stage

git init -q                              # => co-10: a fresh, throwaway repo -- quiet mode, no default-branch chatter
git config user.email "demo@example.com" # => co-10: local commit identity, scoped to THIS repo only
git config user.name "Demo Author"       # => co-10: paired with the email above for every commit below

# co-10: commit 1 -- the correct, original O(n) set-based dedupe. This is the
# repo's KNOWN-GOOD, KNOWN-FAST starting point -- `git bisect good` will later
# point at this exact commit as the last-known-fast revision.
cat >algo.py <<'PYEOF' # => co-10: writes the heredoc body below verbatim to algo.py
def dedupe(items: list[int]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
PYEOF
git add algo.py                                    # => co-10: stages the new file for the first commit
git commit -q -m "commit 1: O(n) set-based dedupe" # => co-10: the KNOWN-GOOD, KNOWN-FAST starting point

# co-10: commit 2 -- documentation only, genuinely unrelated to algo.py's
# runtime. A real bisect run must not be fooled into blaming this commit.
cat >README.md <<'READMEEOF' # => co-10: writes the heredoc body below verbatim to README.md
# algo
A small dedupe utility, benchmarked on every commit.
READMEEOF
git add README.md                       # => co-10: stages the new README
git commit -q -m "commit 2: add README" # => co-10: still correct and fast -- no regression yet

# co-10: commit 3 -- a real DISTRACTOR commit. sed rewrites algo.py in place,
# adding dead code (an unused default arg and an unused helper) with NO effect
# on dedupe()'s own runtime -- the search space stays entirely clean here too.
sed -i.bak 's/def dedupe/def dedupe(items_arg=None):\n    """docstring padding, no behavior change"""\n\n\ndef _unused():\n    pass\n\n\ndef dedupe/' algo.py # => co-10: rewrites algo.py in place
rm -f algo.py.bak                                                                                                                                             # => co-10: sed -i.bak leaves a backup file -- removed so it never gets committed
# co-10: the dead code above is inert -- dedupe() itself is untouched, still O(n)
git add algo.py                                                                      # => co-10: stages the harmless refactor
git commit -q -m "commit 3: harmless refactor (dead code added, no behavior change)" # => co-10: still fast

# co-10: commit 4 -- the SEEDED performance regression itself. dedupe() is
# rewritten to check membership against a growing LIST instead of a SET,
# turning an O(n) function into an accidental O(n^2) one. This is the TRUE
# first-slow commit `git bisect run` is expected to land on.
cat >algo.py <<'PYEOF' # => co-10: overwrites algo.py with the regressed version below
def dedupe(items: list[int]) -> list[int]:
    # PERFORMANCE REGRESSION: switched from a set-based O(n) check to a
    # list-based O(n) "in" check inside an O(n) loop -- O(n^2) overall.
    seen: list[int] = []
    result: list[int] = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result
PYEOF
git add algo.py                                                                       # => co-10: stages the accidental O(n^2) swap
git commit -q -m "commit 4: PERF REGRESSION -- swap set for list (accidental O(n^2))" # => co-10: the TRUE first-slow commit

# co-10: commit 5 -- a second distractor, this time landing AFTER the
# regression. A correct bisect must still isolate commit 4, not this one.
printf '\nSee CHANGELOG for details.\n' >>README.md # => co-10: appends to README.md, algo.py untouched
# co-10: algo.py's own bytes are identical to commit 4's -- only README.md changed here
git add README.md                                   # => co-10: stages the README addition
git commit -q -m "commit 5: unrelated README tweak" # => co-10: a distractor AFTER the bad commit

# co-10: commit 6 -- a trailing, behavior-free comment appended to algo.py
# itself. Even touching the SAME file as the regression must not fool bisect.
echo "# no functional change" >>algo.py # => co-10: appends one comment line, no behavior change
# co-10: dedupe()'s own body is still identical to commit 4's regressed version
git add algo.py                                    # => co-10: stages the trailing comment
git commit -q -m "commit 6: trailing comment only" # => co-10: the repo's current HEAD, known-slow

# co-10: check.sh is the pass/fail oracle `git bisect run` invokes at every
# candidate commit -- its exit code (0 or nonzero) becomes bisect's own
# good/bad signal, so the whole automated search hinges on this one script.
cat >check.sh <<'SHEOF' # => co-10: writes the heredoc body below verbatim to check.sh
#!/usr/bin/env bash
python3 -c "
import sys, time
sys.path.insert(0, '.')
from algo import dedupe

items = list(range(6000)) * 2  # =>  12,000 items, half duplicates
start = time.perf_counter()
dedupe(items)
elapsed_ms = (time.perf_counter() - start) * 1000

THRESHOLD_MS = 50.0
print(f'benchmark: {elapsed_ms:.1f}ms (threshold {THRESHOLD_MS}ms)')
sys.exit(0 if elapsed_ms < THRESHOLD_MS else 1)
"
SHEOF
chmod +x check.sh # => co-10: git bisect run executes this file directly, so it must be executable

# co-10: setup is complete -- the 6-commit history below is what a real
# `git bisect run bash check.sh` session bisects through next.
echo "repo ready -- 6 commits, perf regression seeded at commit 4" # => confirms setup finished
git log --oneline                                                  # => co-10: shows the 6-commit history a reader is about to bisect through
