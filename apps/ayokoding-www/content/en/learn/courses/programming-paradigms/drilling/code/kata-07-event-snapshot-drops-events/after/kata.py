"""Kata 7 (after): event-driven fix -- draining the live queue processes events added during dispatch too."""


def run_dispatcher(initial_events: list[str]) -> list[str]:
    queue = list(initial_events)
    processed: list[str] = []
    while queue:  # keeps going as long as ANY event -- including ones added mid-dispatch -- remains
        event = queue.pop(0)
        processed.append(event)
        if event == "signup":
            queue.append("welcome_email")
    return processed


print(run_dispatcher(["signup", "login"]))
