"""Example 75: pytest verification for `Barrier`-Synchronized Phased Computation."""

from example import run_phased_computation


def test_no_worker_starts_phase_two_before_every_worker_finishes_phase_one() -> None:
    phase1_end, phase2_start = run_phased_computation()
    assert min(phase2_start) >= max(phase1_end)  # => the barrier genuinely enforced the phase boundary


# => Run: pytest -- Output: 1 passed
