"""Kata 10 (before): boolean-flag soup lets a task be marked complete without ever being assigned."""


class Task:
    def __init__(self) -> None:
        self.is_assigned = False
        self.is_completed = False

    def complete(self) -> None:
        self.is_completed = True  # BUG: nothing checks is_assigned first


task = Task()
task.complete()  # marked complete WITHOUT ever being assigned to anyone
print(task.is_assigned, task.is_completed)
