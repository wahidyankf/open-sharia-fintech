"""Example 33: profile ONCE to a .prof file, then read it back sorted TWO different ways."""

from __future__ import annotations

import cProfile
import pstats
from pstats import SortKey

from inventory import run

cProfile.run("run()", "inventory.prof")

stats = pstats.Stats("inventory.prof")
print("=== sorted by TIME (tottime -- a function's OWN time, excluding callees) ===")
stats.sort_stats(SortKey.TIME).print_stats(4)
print(
    "=== sorted by CUMULATIVE (cumtime -- includes time spent in everything it calls) ==="
)
stats.sort_stats(SortKey.CUMULATIVE).print_stats(4)
