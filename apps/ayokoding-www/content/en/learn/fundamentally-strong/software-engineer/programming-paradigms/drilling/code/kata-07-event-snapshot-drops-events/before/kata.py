"""Kata 7 (before): event-driven violation -- a snapshot iteration drops events fired during processing."""


def run_dispatcher(initial_events: list[str]) -> list[str]:
    queue = list(initial_events)
    processed: list[str] = []
    for event in list(queue):  # SMELL: `list(queue)` takes a frozen snapshot at loop start
        processed.append(event)
        if event == "signup":
            queue.append("welcome_email")  # BUG: appended to `queue`, but the loop iterates the SNAPSHOT, not `queue`
    return processed


print(run_dispatcher(["signup", "login"]))
