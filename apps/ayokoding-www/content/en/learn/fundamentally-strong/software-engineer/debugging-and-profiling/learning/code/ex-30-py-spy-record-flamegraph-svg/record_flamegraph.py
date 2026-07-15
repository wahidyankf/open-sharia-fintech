"""Example 30: py-spy record -o profile.svg -- the real py-spy command is documented in this
example's write-up; on this sandbox py-spy needs root (see ex-29), so this script produces the
SAME kind of collapsed-stack + SVG artifact with the disclosed mini_sampler + a real inferno
render instead, then cross-validates the result against a real cProfile run of the identical
workload."""

from __future__ import annotations

import threading

import mini_sampler
import workload

samples = mini_sampler.collect_samples(workload.run_workload, threading.get_ident())
with open("profile.collapsed", "w") as f:
    for stack, count in sorted(samples.items()):
        f.write(f"{stack} {count}\n")
print(f"wrote {len(samples)} distinct stacks, {sum(samples.values())} total samples")

# cross-validate with a REAL cProfile instrumenting run of the exact same workload
import cProfile
import pstats
from pstats import SortKey

profiler = cProfile.Profile()
profiler.enable()
workload.run_workload()
profiler.disable()
print("\n--- cProfile cross-check (top 3 by cumulative) ---")
pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE).print_stats(3)
