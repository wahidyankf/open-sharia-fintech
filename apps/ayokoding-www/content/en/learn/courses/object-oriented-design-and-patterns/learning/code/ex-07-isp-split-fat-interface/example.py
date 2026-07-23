"""Example 7: Split a Fat Worker Interface."""

from typing import Protocol  # => Protocol declares each role as a small, focused shape


class Workable(Protocol):  # => a role interface: ONLY the ability to work
    def work(self) -> str:  # => the one method this role requires
        ...  # => Protocol methods have no body -- a structural contract only


class Eatable(Protocol):  # => a SEPARATE role interface: ONLY the ability to eat
    def eat(self) -> str:  # => the one method this role requires
        ...  # => Protocol methods have no body -- a structural contract only


class HumanWorker:  # => a human genuinely satisfies BOTH roles
    def work(self) -> str:  # => satisfies Workable
        return "human works"  # => a real, honest implementation

    def eat(self) -> str:  # => satisfies Eatable
        return "human eats"  # => a real, honest implementation


class RobotWorker:  # => a robot satisfies ONLY Workable -- eat() would be a lie
    def work(self) -> str:  # => satisfies Workable, nothing more
        return "robot works"  # => a real, honest implementation


def run_shift(worker: Workable) -> str:  # => a client depending on the SMALL role only
    return worker.work()  # => never asks for eat() -- RobotWorker fits perfectly


print(run_shift(HumanWorker()))  # => a human satisfies the narrow Workable role too
print(run_shift(RobotWorker()))  # => a robot needs no eat() method to pass here
# => Output: human works
# => robot works
# => Before the split, a single fat `Worker` interface would have forced `RobotWorker` to also implement `eat()`
