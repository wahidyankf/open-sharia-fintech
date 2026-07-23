"""Example 59: pytest verification for GIL vs Free-Threaded Benchmarking."""

import shutil
import sys

from example import benchmark_current_interpreter, benchmark_other_interpreter, gil_is_enabled


def test_current_interpreter_speedup_matches_its_own_gil_status() -> None:
    speedup = benchmark_current_interpreter()
    if gil_is_enabled():
        assert speedup < 2.0  # => the standard build in this environment does not parallelize CPU work
    else:
        assert speedup > 2.5  # => a free-threaded build genuinely parallelizes CPU work


def test_free_threaded_binary_lookup_does_not_raise() -> None:
    # => shutil.which must always return either a path string or None -- never raise
    result = shutil.which("python3.14t")
    assert result is None or isinstance(result, str)


def test_benchmark_other_interpreter_reuses_this_script_via_the_same_interpreter() -> None:
    # => no python3.14t is installed here, so this points `benchmark_other_interpreter` at THIS
    # => interpreter's own binary instead -- proving the "--benchmark-only" reuse mechanism works
    speedup = benchmark_other_interpreter(sys.executable)
    assert speedup > 0.0  # => a real, positive speedup number was successfully parsed from stdout


# => Run: pytest -- Output: 3 passed
