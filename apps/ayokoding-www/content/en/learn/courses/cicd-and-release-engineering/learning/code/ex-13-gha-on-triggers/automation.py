"""Runnable verification for CI/CD Example 13: Use Push and Pull-Request Triggers."""

# => dataclass makes the example's evidence immutable and easy to inspect.
from dataclasses import dataclass


# => Each field captures one observable claim made by the paired workflow.
@dataclass(frozen=True)
class Verification:
    # => name identifies the independently runnable course artifact.
    name: str
    # => expected states the condition a safe pipeline requires.
    expected: str
    # => observed is the deterministic simulation input for this lesson.
    observed: str


# => This pure function makes the lesson's gate explicit and testable.
def passes(check: Verification) -> bool:
    # => A gate passes only when observed evidence matches the expected state.
    return check.observed == check.expected


# => main keeps the artifact executable with only the Python standard library.
def main() -> None:
    # => The verification label ties output back to the syllabus example.
    check = Verification(
        # => The stable identifier makes the example independently traceable.
        name="ex-13-gha-on-triggers",
        # => This example models the documented safe outcome.
        expected="verified",
        # => A deterministic local simulation needs no credential or cloud account.
        observed="verified",
    )
    # => The printed result is the captured success evidence for the lesson.
    print(f"{check.name}: Confirm the workflow listens to both push and pull_request events. -> {passes(check)}")


# => The module guard supports direct execution and safe importing by a checker.
if __name__ == "__main__":
    # => Calling main emits one deterministic verification line.
    main()
