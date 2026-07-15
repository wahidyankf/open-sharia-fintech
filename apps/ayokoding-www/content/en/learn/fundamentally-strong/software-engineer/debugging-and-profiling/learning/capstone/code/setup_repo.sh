#!/usr/bin/env bash
# Capstone: a 6-commit repo carrying a seeded CORRECTNESS bug (a KeyError,
# introduced at commit 4) in an order-processing pipeline. The performance bug
# (an O(n^2) dedupe in the SAME pipeline) is present from the start and is
# fixed separately in the profiling half of the capstone (steps 3-4), not via
# git bisect -- per the capstone spec, only the correctness bug is bisected.
set -euo pipefail # => co-09/co-10: fail fast on any error, unset variable, or failed pipe stage

git init -q                              # => co-09: a fresh, throwaway repo -- quiet mode, no default-branch chatter
git config user.email "demo@example.com" # => co-09: local commit identity, scoped to THIS repo only
git config user.name "Demo Author"       # => co-09: paired with the email above for every commit below

# co-09: commit 1 -- the correct, original pipeline. The repo's KNOWN-GOOD
# starting point for the correctness bisect below. dedupe_customers is
# ALREADY O(n^2) here -- that performance bug is present from commit 1 and is
# fixed separately in steps 3-4, not by bisecting.
#
# co-01: three functions, in a small call chain: compute_total() (the
# correctness bug's future home), dedupe_customers() (the performance bug's
# home, unchanged across every commit below), and build_customer_report()
# (the public entry point every check script and profile below calls into).
cat >pipeline.py <<'PYEOF' # => co-09: writes the heredoc body below verbatim to pipeline.py
from __future__ import annotations


def compute_total(order: dict) -> float:
    return order["price"] * order["qty"] - order.get("discount", 0.0)


def dedupe_customers(orders: list[dict]) -> list[dict]:
    seen: list[str] = []
    result: list[dict] = []
    for order in orders:
        customer_id = order["customer_id"]
        if customer_id not in seen:
            seen.append(customer_id)
            result.append(order)
    return result


def build_customer_report(orders: list[dict]) -> list[dict]:
    unique_customers = dedupe_customers(orders)
    return [{"customer_id": o["customer_id"], "total": compute_total(o)} for o in unique_customers]
PYEOF
git add pipeline.py                                                                                   # => co-09: stages the new file for the first commit
git commit -q -m "commit 1: order pipeline -- compute_total, dedupe_customers, build_customer_report" # => co-09: KNOWN-GOOD start

# co-09/co-23: commit 2 -- the regression test itself, added BEFORE the
# correctness bug it will later catch (test-first: the guard predates the fault).
#
# co-23: two tests -- one for the WITH-discount case (always passed, on
# every commit below) and one for the WITHOUT-discount case (the one that
# will go red at commit 4 and stay red until the debugger-guided fix).
cat >test_pipeline.py <<'PYEOF' # => co-09: writes the heredoc body below verbatim to test_pipeline.py
from pipeline import compute_total


def test_compute_total_with_discount():
    assert compute_total({"price": 10.0, "qty": 2, "discount": 3.0}) == 17.0


def test_compute_total_without_discount():
    assert compute_total({"price": 10.0, "qty": 2}) == 20.0
PYEOF
git add test_pipeline.py                          # => co-09: stages the new regression test file
git commit -q -m "commit 2: add regression tests" # => co-09: still correct -- both tests pass here too

# co-09: commit 3 -- documentation only, genuinely unrelated to pipeline.py's behavior.
echo "# pipeline" >README.md                        # => co-09: creates a minimal README -- a real distractor commit
git add README.md                                   # => co-09: stages the new README
git commit -q -m "commit 3: add README (unrelated)" # => co-09: correctness bug not yet introduced

# co-09/co-04: commit 4 -- the SEEDED CORRECTNESS bug -- compute_total now
# REQUIRES a "discount" key instead of defaulting it to 0.0. This is the TRUE
# first-bad commit the correctness bisect below is expected to land on.
#
# co-04: dedupe_customers() and build_customer_report() are BYTE-IDENTICAL to
# commit 1's versions here -- only compute_total()'s body changed, from a
# safe .get(..., 0.0) default to a bare, KeyError-prone dict index.
cat >pipeline.py <<'PYEOF' # => co-09: overwrites pipeline.py with the KeyError-prone version below
from __future__ import annotations


def compute_total(order: dict) -> float:
    # CORRECTNESS BUG: assumes "discount" is always present -- KeyError on
    # orders that legitimately have no discount.
    return order["price"] * order["qty"] - order["discount"]


def dedupe_customers(orders: list[dict]) -> list[dict]:
    seen: list[str] = []
    result: list[dict] = []
    for order in orders:
        customer_id = order["customer_id"]
        if customer_id not in seen:
            seen.append(customer_id)
            result.append(order)
    return result


def build_customer_report(orders: list[dict]) -> list[dict]:
    unique_customers = dedupe_customers(orders)
    return [{"customer_id": o["customer_id"], "total": compute_total(o)} for o in unique_customers]
PYEOF
git add pipeline.py                                                                 # => co-09: stages the seeded correctness bug
git commit -q -m "commit 4: CORRECTNESS BUG -- compute_total requires discount key" # => co-09/co-04: the TRUE first-bad commit

# co-09: commit 5 -- a distractor landing AFTER the bug. A correct bisect must
# still isolate commit 4, not this one.
printf '\nProcesses a batch of orders into a per-customer report.\n' >>README.md # => co-09: appends to README.md only
git add README.md                                                                # => co-09: stages the README expansion
git commit -q -m "commit 5: expand README (unrelated)"                           # => co-09: a distractor AFTER the bad commit

# co-09: commit 6 -- a trailing, behavior-free comment appended to pipeline.py
# itself. Even touching the SAME file as the bug must not fool bisect.
echo "# stable" >>pipeline.py                      # => co-09: appends one comment line, no behavior change
git add pipeline.py                                # => co-09: stages the trailing comment
git commit -q -m "commit 6: trailing comment only" # => co-09: the repo's current HEAD, correctness bug still present

# co-09: setup is complete -- the 6-commit history below is what the capstone's
# `git bisect run bash check_bisect.sh` bisects through next.
#
# co-09/co-10: three distractor commits (2, 3, 5, 6) surround the ONE real
# correctness bug (commit 4) -- a correct bisect must ignore all four of them.
echo "repo ready -- correctness bug (KeyError) at commit 4" # => confirms setup finished
git log --oneline                                           # => co-09: shows the 6-commit history a reader is about to bisect through
