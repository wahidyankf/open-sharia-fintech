"""Capstone step 2: debugger-guided root-cause confirmation via pdb post-mortem
on the minimized failing case from step 1."""

import sys  # => co-01: unused directly, kept to mirror this capstone's other scripts' import style
from pipeline import (
    compute_total,
)  # => co-01/co-03: the SAME function whose KeyError this post-mortem session confirms

order = {
    "customer_id": "cust-special-217",
    "price": 12.5,
    "qty": 2,
}  # => co-11: the minimized repro from step 1, verbatim
compute_total(
    order
)  # => co-01/co-03: the ONE call whose uncaught KeyError drives the post-mortem session below
