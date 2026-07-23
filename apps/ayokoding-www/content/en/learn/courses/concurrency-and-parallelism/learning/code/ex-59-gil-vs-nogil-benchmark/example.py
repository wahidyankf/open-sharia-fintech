"""Example 59: Benchmarking IDENTICAL Threaded Code -- GIL Build vs `python3.14t`."""

import shutil  # => shutil.which locates a `python3.14t` binary on PATH, if one is installed
import subprocess  # => runs THIS SAME script under a DIFFERENT interpreter, if one is found
import sys  # => co-04: distinguishes the CURRENTLY running interpreter's own GIL status
import threading  # => the identical threaded-CPU shape used throughout this topic (ex-03, ex-49, ex-58)
import time  # => measures wall time for the empirical speedup ratio

ITERATIONS = 5_000_000  # => tuned so 4 threads' worth of work is clearly measurable
THREAD_COUNT = 4  # => how many threads race to do CPU work concurrently


def gil_is_enabled() -> bool:  # => the SAME version-gated check as ex-04 and ex-58
    if hasattr(sys, "_is_gil_enabled"):  # => only exists on Python 3.13+
        return sys._is_gil_enabled()  # pyright: ignore[reportPrivateUsage]
        # => leading underscore is CPython's naming, not a privacy signal -- the documented 3.13+ API
    return True  # => pre-3.13: no free-threaded option ever existed


def cpu_task(n: int) -> int:  # => pure CPU work -- no I/O, so any GIL present can NEVER release mid-loop
    total = 0  # => accumulator -- forces real interpreter bytecode execution
    for i in range(n):  # => a tight loop -- exactly the shape a GIL serializes across threads
        total += i  # => trivial arithmetic; only the TIME this takes matters here
    return total  # => the actual value is irrelevant to this example


def benchmark_current_interpreter() -> float:
    single_start = time.perf_counter()  # => single_start: wall time before the ONE-thread baseline unit
    cpu_task(ITERATIONS)  # => runs exactly ONE unit of work, alone, to establish a per-unit baseline
    single_time = time.perf_counter() - single_start  # => single_time: how long ONE unit takes, uncontended

    threads = [threading.Thread(target=cpu_task, args=(ITERATIONS,)) for _ in range(THREAD_COUNT)]
    # => threads: THREAD_COUNT independent threads, all racing to run the SAME cpu_task concurrently
    start = time.perf_counter()  # => start: wall time before the THREAD_COUNT-way concurrent run
    for t in threads:  # => starts every thread
        t.start()  # => each begins its own ITERATIONS-long loop, "concurrently"
    for t in threads:  # => waits for every thread to finish
        t.join()  # => join() blocks until that thread's cpu_task() call returns
    elapsed = time.perf_counter() - start  # => elapsed: wall time for ALL THREAD_COUNT threads combined
    return (single_time * THREAD_COUNT) / elapsed  # => speedup: how much faster the threaded run was vs serial


def benchmark_other_interpreter(binary_path: str) -> float:
    # => re-runs THIS EXACT FILE under `binary_path`, in "print-only" mode -- one source, two interpreters
    args = [binary_path, __file__, "--benchmark-only"]  # => args: launches THIS module with the parse-friendly flag
    completed = subprocess.run(args, capture_output=True, text=True, check=True, timeout=30)  # => a real subprocess run
    return float(completed.stdout.strip())  # => parses the single number the child process printed


if __name__ == "__main__":  # => module entry point
    if "--benchmark-only" in sys.argv:  # => the mode `benchmark_other_interpreter` invokes via subprocess
        print(f"{benchmark_current_interpreter():.4f}")  # => prints JUST the number -- nothing else, for easy parsing
    else:  # => the normal, full demonstration mode
        current_speedup = benchmark_current_interpreter()  # => current_speedup: THIS interpreter's own measured ratio
        current_gil_enabled = gil_is_enabled()  # => current_gil_enabled: is THIS interpreter's GIL active?
        print(f"current_build: gil_enabled={current_gil_enabled} speedup={current_speedup:.2f}x")

        free_threaded_binary = shutil.which("python3.14t")  # => resolved path to `python3.14t`, or None
        if free_threaded_binary is None:  # => the case in THIS environment -- no free-threaded build installed
            print("python3.14t not found on PATH -- skipping the live cross-build comparison here")
            # => this is the ONLY branch actually exercised when this file is verified in this repo
            print("on a machine with python3.14t installed, rerunning THIS SAME script under it would print >2.5x")
        else:  # => the case on a machine where a reader HAS installed python3.14t alongside standard CPython
            free_threaded_speedup = benchmark_other_interpreter(free_threaded_binary)  # => genuinely re-benchmarks
            print(f"free_threaded_build: speedup={free_threaded_speedup:.2f}x")  # => the OTHER build's own result
            assert free_threaded_speedup > 2.5  # => confirms the t-build genuinely parallelized the identical code

        # => Only a `python3.14t` (PEP 703/779, free-threaded) build can genuinely run 4 CPU-bound Python
        # => threads across 4 cores: it removes the single GIL that otherwise serializes bytecode
        # => execution across every thread in a process (co-04). Benchmarking IDENTICAL threaded code on
        # => a standard build shows barely any speedup (this is CPU-bound, so co-05's I/O-release case
        # => doesn't apply); on a free-threaded build, the exact same code scales close to linearly.
        if current_gil_enabled:  # => this environment's actual branch
            assert current_speedup < 2.0  # => confirms the standard GIL build did NOT meaningfully parallelize
        else:  # => the branch a reader running THIS SAME script under python3.14t would take
            assert current_speedup > 2.5  # => confirms a free-threaded interpreter DID scale close to linearly
        print("ex-59 OK")  # => Output: ex-59 OK
