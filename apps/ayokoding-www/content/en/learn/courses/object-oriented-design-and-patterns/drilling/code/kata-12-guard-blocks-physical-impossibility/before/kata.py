"""Kata 12 (before): a state transition without a guard can fire even when a real precondition is false."""


class DoorLock:
    def __init__(self) -> None:
        self.state = "locked"
        self.battery_level = 0  # dead battery -- physically CANNOT actuate the lock

    def unlock(self) -> None:
        self.state = "unlocked"  # BUG: no guard checks battery_level before flipping state


lock = DoorLock()
lock.unlock()
print(lock.state)  # claims "unlocked" even though the battery is dead and nothing physically moved
