#!/usr/bin/env bash
# Capstone step 1: git bisect run's pass/fail oracle -- exit 1 means this
# commit still raises the seeded KeyError, exit 0 means the batch built clean.
python3 -c "
import sys  # needed for sys.path.insert and sys.exit below
sys.path.insert(0, '.')  # makes the repo's own pipeline.py/make_failing_batch.py importable
from pipeline import build_customer_report  # the function whose KeyError this oracle checks for
from make_failing_batch import make_failing_batch  # the SAME 400-order batch that seeds the bug

orders = make_failing_batch()  # the same 400-order batch that seeds the bug
try:  # wraps the ONE call whose KeyError is this oracle's actual signal
    build_customer_report(orders)  # the SAME pipeline entry point this whole capstone bisects against
except KeyError:  # co-04: this specific exception type IS the seeded correctness bug
    sys.exit(1)  # BAD -- this commit still has the correctness bug
sys.exit(0)  # GOOD -- this commit builds the report without a KeyError
"
