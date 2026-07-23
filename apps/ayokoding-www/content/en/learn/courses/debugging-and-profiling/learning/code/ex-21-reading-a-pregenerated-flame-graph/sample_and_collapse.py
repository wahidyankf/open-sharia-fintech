"""A minimal, self-built sampling profiler -- periodically reads the main thread's real call stack
via sys._current_frames() from a background thread, and writes collapsed-stack lines
("func_a;func_b;func_c count") in the same folded-stack format py-spy/inferno's own
inferno-collapse-* tools produce. This exists ONLY so this example can render a genuine flame graph
SVG without needing py-spy's root privilege on this sandbox (see the Intermediate tier's py-spy
examples for the real py-spy CLI and its own macOS root requirement) -- every sample below is a real
stack captured from the real workload.py process while it actually ran.
"""

from __future__ import annotations

import sys
import threading
import time
from collections import Counter

import workload

SAMPLE_INTERVAL_S = 0.001
samples: Counter[str] = Counter()
stop_flag = threading.Event()


def sampler(target_thread_id: int) -> None:
    while not stop_flag.is_set():
        frame = sys._current_frames().get(target_thread_id)
        stack: list[str] = []
        while frame is not None:
            stack.append(frame.f_code.co_name)
            frame = frame.f_back
        stack.reverse()
        samples[";".join(stack)] += 1
        time.sleep(SAMPLE_INTERVAL_S)


def run_sampler_harness() -> None:
    main_thread_id = threading.get_ident()
    sampler_thread = threading.Thread(
        target=sampler, args=(main_thread_id,), daemon=True
    )
    sampler_thread.start()
    time.sleep(0.05)  # let the sampler thread fully start before the workload begins
    workload.run_workload()
    stop_flag.set()
    sampler_thread.join()

    with open("profile.collapsed", "w") as f:
        for stack, count in sorted(samples.items()):
            f.write(f"{stack} {count}\n")
    print(
        f"wrote {len(samples)} distinct stacks, {sum(samples.values())} total samples"
    )


if __name__ == "__main__":
    run_sampler_harness()
