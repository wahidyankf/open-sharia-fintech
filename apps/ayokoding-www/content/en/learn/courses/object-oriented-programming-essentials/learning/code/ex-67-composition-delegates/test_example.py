"""Example 67: pytest verification for A Service Delegates to a Logger Collaborator."""

from example import Logger, Service, SilentLogger


def test_swapping_the_collaborator_changes_observed_behavior() -> None:
    loud: Service = Service(Logger())
    quiet: Service = Service(
        SilentLogger()
    )  # => structurally compatible, accepted cleanly
    assert loud.run() == "[LOG] service ran"
    assert (
        quiet.run() == ""
    )  # => same Service code, a different collaborator, different behavior


# => Run: pytest -- Output: 1 passed
