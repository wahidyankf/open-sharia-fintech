"""Example 7: pytest verification for Split a Fat Worker Interface."""

from example import HumanWorker, RobotWorker, run_shift


def test_robot_worker_implements_only_workable() -> None:
    # => the mechanical proof: RobotWorker has work() but genuinely lacks eat()
    assert hasattr(RobotWorker, "work")  # => satisfies the Workable role
    assert not hasattr(RobotWorker, "eat")  # => never forced to fake an Eatable role


def test_human_worker_still_satisfies_both_roles() -> None:
    assert hasattr(HumanWorker, "work") and hasattr(HumanWorker, "eat")  # => a human genuinely does both
    assert run_shift(HumanWorker()) == "human works"
    assert run_shift(RobotWorker()) == "robot works"  # => both fit the narrow role


# => Run: pytest -- Output: 2 passed
