"""A minimal, self-built sampling profiler used across this tier's py-spy-flavored examples --
periodically reads a thread's real call stack via sys._current_frames() from a background
thread. This exists ONLY because py-spy requires root on this sandbox's macOS host ("OSX always
requires running as root" -- py-spy's own README FAQ, github.com/benfred/py-spy). Every sample
this module records is a real stack captured from the real target process while it actually ran;
this is NOT py-spy itself, and is labeled as such everywhere it is used.
"""

from __future__ import annotations

import sys
import threading
import time
from collections import Counter


def collect_samples(
    target_fn, target_thread_id: int, interval_s: float = 0.001
) -> Counter[str]:
    samples: Counter[str] = Counter()
    stop_flag = threading.Event()

    def sampler() -> None:
        while not stop_flag.is_set():
            frame = sys._current_frames().get(target_thread_id)
            stack: list[str] = []
            while frame is not None:
                stack.append(frame.f_code.co_name)
                frame = frame.f_back
            stack.reverse()
            samples[";".join(stack)] += 1
            time.sleep(interval_s)

    sampler_thread = threading.Thread(target=sampler, daemon=True)
    sampler_thread.start()
    time.sleep(0.02)
    target_fn()
    stop_flag.set()
    sampler_thread.join()
    return samples
