# Errors cross the tool boundary as typed observations.
from dataclasses import dataclass

# Union preserves this annotation on the project's Python 3.9-compatible interpreter.
from typing import Union


# The error keeps a machine-readable category and safe message.
@dataclass(frozen=True)
class ErrorResult:
    # False distinguishes this branch from a successful result.
    ok: bool
    # The code supports deterministic recovery policy.
    code: str
    # The message explains the immediate problem.
    message: str


# This tool models a recoverable arithmetic failure.
def divide(left: int, right: int) -> Union[int, ErrorResult]:
    # Never let a known invalid operation escape as an opaque exception.
    if right == 0:
        return ErrorResult(False, "DIVIDE_BY_ZERO", "right must not be zero")
    # Valid input follows the normal computation path.
    return left // right


# The structured error is safe to return to a model.
assert divide(4, 0).code == "DIVIDE_BY_ZERO"  # type: ignore[union-attr]
# Print the explicit recovery signal.
print(divide(4, 0))
