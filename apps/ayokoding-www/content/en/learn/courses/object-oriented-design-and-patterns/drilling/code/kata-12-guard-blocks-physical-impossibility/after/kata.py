"""Kata 12 (after): a guard blocks the transition when the real precondition (battery_level > 0) is not met."""


class GuardBlocked(Exception):
    pass


class DoorLock:
    def __init__(self) -> None:
        self.state = "locked"
        self.battery_level = 0

    def unlock(self) -> None:
        if self.battery_level <= 0:  # => the GUARD -- checked in addition to any transition-table entry
            raise GuardBlocked("cannot unlock: battery is dead")
        self.state = "unlocked"


lock = DoorLock()
try:
    lock.unlock()
except GuardBlocked as error:
    print(error)
print(lock.state)  # correctly still "locked" -- the guard prevented the state from lying about reality
