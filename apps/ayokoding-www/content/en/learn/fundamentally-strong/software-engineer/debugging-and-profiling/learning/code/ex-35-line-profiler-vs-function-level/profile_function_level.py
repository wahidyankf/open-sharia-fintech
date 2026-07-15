"""Example 35: cProfile's view -- attributes cost to the WHOLE function, not any one line."""

from __future__ import annotations

import cProfile
import pstats
from pstats import SortKey

from merge_report import build_merged_report

profiler = cProfile.Profile()
profiler.enable()
build_merged_report(list(range(3000)), list(range(1500, 4500)))
profiler.disable()
pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE).print_stats(3)
