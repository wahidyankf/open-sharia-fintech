"""Example 28: the INSTRUMENTING side -- exact per-call counts via cProfile (co-13)."""

from __future__ import annotations

import cProfile
import pstats
from pstats import SortKey

from workload import run_workload

profiler = cProfile.Profile()
profiler.enable()
run_workload()
profiler.disable()
pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE).print_stats(5)
