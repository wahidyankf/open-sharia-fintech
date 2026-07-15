#!/usr/bin/env bash
# Example 79: a 6-commit repo with a real regression at commit 4, where the
# check ITSELF is deliberately flaky (~20% false-pass rate even on bad
# commits) -- check.sh retries N times and reports bad only on a majority,
# guarding git bisect against being misled by the flakiness.
set -euo pipefail # => co-10/co-20: fail fast on any error, unset variable, or failed pipe stage

git init -q                              # => co-10: a fresh, throwaway repo -- quiet mode, no default-branch chatter
git config user.email "demo@example.com" # => co-10: local commit identity, scoped to THIS repo only
git config user.name "Demo Author"       # => co-10: paired with the email above for every commit below

# co-10: commit 1 -- the correct, original implementation. The repo's
# KNOWN-GOOD starting point for the bisect below.
cat >calc.py <<'PYEOF' # => co-10: writes the heredoc body below verbatim to calc.py
def compute(x: int) -> int:
    return x * 2
PYEOF
git add calc.py                                 # => co-10: stages the new file for the first commit
git commit -q -m "commit 1: compute(x) = x * 2" # => co-10: the KNOWN-GOOD starting point

# co-10: commit 2 -- documentation only, genuinely unrelated to calc.py's own behavior.
echo "# calc" >README.md                # => co-10: creates a minimal README -- a real distractor commit
git add README.md                       # => co-10: stages the new README
git commit -q -m "commit 2: add README" # => co-10: still correct -- calc.py is untouched here

# co-10: commit 3 -- a second, harmless distractor -- more README text, still
# no change to calc.py at all.
printf '\nA tiny doubling helper.\n' >>README.md # => co-10: appends to README.md -- calc.py untouched
git add README.md                                # => co-10: stages the README expansion
git commit -q -m "commit 3: expand README"       # => co-10: still correct -- a second distractor commit before the regression

# co-10/co-20: commit 4 -- the SEEDED regression itself -- an off-by-one. This
# is the TRUE first-bad commit the guarded bisect below is expected to land on,
# DESPITE check.sh's own deliberate ~20% false-pass flakiness.
cat >calc.py <<'PYEOF' # => co-10: overwrites calc.py with the off-by-one version below
def compute(x: int) -> int:
    # REGRESSION: off-by-one
    return x * 2 + 1
PYEOF
git add calc.py                                                    # => co-10: stages the seeded regression
git commit -q -m "commit 4: REGRESSION -- off-by-one in compute()" # => co-10/co-20: the TRUE first-bad commit

# co-10: commit 5 -- a distractor landing AFTER the regression. A correct
# (guarded) bisect must still isolate commit 4, not this one.
printf '\nSee CHANGELOG.\n' >>README.md             # => co-10: appends to README.md, calc.py untouched
git add README.md                                   # => co-10: stages the README addition
git commit -q -m "commit 5: unrelated README tweak" # => co-10: a distractor AFTER the bad commit

# co-10: commit 6 -- a trailing, behavior-free comment appended to calc.py
# itself. Even touching the SAME file as the regression must not fool bisect.
echo "# stable" >>calc.py                          # => co-10: appends one comment line, no behavior change
git add calc.py                                    # => co-10: stages the trailing comment
git commit -q -m "commit 6: trailing comment only" # => co-10: the repo's current HEAD, regression still present

# co-10/co-20: check.sh is the pass/fail oracle -- deliberately FLAKY, so a
# naive `git bisect run bash check.sh` alone could be misled by a false pass.
cat >check.sh <<'SHEOF' # => co-20: writes the heredoc body below verbatim to check.sh
#!/usr/bin/env bash
# co-20: FLAKY on purpose -- uses a per-invocation random seed derived from the
# current time, so ~20% of individual attempts FALSELY pass even on a bad
# commit (simulating a genuinely flaky test in CI).
python3 -c "
import random, sys
sys.path.insert(0, '.')
from calc import compute

random.seed()  # unseeded -- genuinely different each process invocation
real_result = compute(5)
flaky_false_pass = random.random() < 0.2  # ~20% chance of a FALSE pass
if flaky_false_pass:
    sys.exit(0)
sys.exit(0 if real_result == 10 else 1)
"
SHEOF
chmod +x check.sh # => co-20: git bisect run executes this file directly, so it must be executable

# co-10/co-20: check_guarded.sh wraps the SAME flaky check.sh in a majority
# vote across N retries -- the real fix for a flaky bisect oracle.
cat >check_guarded.sh <<'SHEOF' # => co-10: writes the heredoc body below verbatim to check_guarded.sh
#!/usr/bin/env bash
# co-10/co-20: retry the (flaky) check N times, report BAD only if a MAJORITY
# of attempts fail -- guards git bisect against the ~20% false-pass rate.
N=7
fail_count=0
for i in $(seq 1 "$N"); do
    if ! ./check.sh; then
        fail_count=$((fail_count + 1))
    fi
done
majority=$(( (N / 2) + 1 ))
echo "check_guarded: $fail_count/$N attempts failed (need $majority for BAD)"
if [ "$fail_count" -ge "$majority" ]; then
    exit 1
fi
exit 0
SHEOF
chmod +x check_guarded.sh # => co-10: git bisect run executes THIS file directly, not the flaky check.sh alone

# co-10/co-20: setup is complete -- the 6-commit history below is what a real
# `git bisect run bash check_guarded.sh` bisects through next.
echo "repo ready -- regression at commit 4, check.sh is ~20% flaky, check_guarded.sh majority-votes" # => confirms setup finished
git log --oneline                                                                                    # => co-10: shows the 6-commit history a reader is about to bisect through
