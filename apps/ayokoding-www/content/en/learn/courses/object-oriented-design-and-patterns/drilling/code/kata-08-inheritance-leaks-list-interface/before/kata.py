"""Kata 8 (before): naive inheritance leaks list's full interface, letting sort() silently reorder events."""


class EventLog(list):  # SMELL: is-a list -- inherits EVERY list method, including sort()
    def record(self, event: str) -> None:
        self.append(event)


log = EventLog()
log.record("login")
log.record("purchase")
log.record("logout")
log.sort()  # BUG: nothing stops a caller from calling a leaked list method that breaks chronological order
print(log)
