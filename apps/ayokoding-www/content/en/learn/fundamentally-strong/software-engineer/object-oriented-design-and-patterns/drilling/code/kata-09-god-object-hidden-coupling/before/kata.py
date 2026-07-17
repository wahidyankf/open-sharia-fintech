"""Kata 9 (before): god object -- one class mixes validation, persistence, AND notification, so a validation-only call also writes."""


class UserManager:  # SMELL: one class handles validation, persistence, AND notification
    def __init__(self) -> None:
        self.database: list[str] = []
        self.notifications: list[str] = []
        self._pending: str | None = None  # shared mutable state -- the root of the coupling below

    def is_valid_email(self, email: str) -> bool:
        self._pending = email  # SMELL: a "just validate" call has a SIDE EFFECT of staging a save
        return "@" in email

    def save(self) -> None:
        if self._pending is not None:
            self.database.append(self._pending)
            self.notifications.append(f"welcome {self._pending}")


manager = UserManager()
manager.is_valid_email("not-an-email")  # caller only wanted to CHECK validity...
manager.save()  # ...but a later, unrelated save() call now persists the INVALID email anyway
print(manager.database)
