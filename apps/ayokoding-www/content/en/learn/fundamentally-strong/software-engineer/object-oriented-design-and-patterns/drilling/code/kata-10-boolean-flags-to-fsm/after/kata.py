"""Kata 10 (after): a transition-table FSM makes "complete without assign" structurally illegal."""


class IllegalTransition(Exception):
    pass


TASK_TRANSITIONS: dict[tuple[str, str], str] = {
    ("open", "assign"): "assigned",
    ("assigned", "complete"): "completed",
}


class Task:
    def __init__(self) -> None:
        self.state = "open"

    def send(self, event: str) -> None:
        key = (self.state, event)
        if key not in TASK_TRANSITIONS:
            raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}")
        self.state = TASK_TRANSITIONS[key]


task = Task()
try:
    task.send("complete")  # attempting the SAME illegal move as the before-script
except IllegalTransition as error:
    print(error)
