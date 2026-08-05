"""Explain restart behavior for failures but not clean exits."""

exit_statuses = {"clean shutdown": 0, "uncaught failure": 1}
for event, status in exit_statuses.items():
    print(event, "restart" if status != 0 else "do not restart")
