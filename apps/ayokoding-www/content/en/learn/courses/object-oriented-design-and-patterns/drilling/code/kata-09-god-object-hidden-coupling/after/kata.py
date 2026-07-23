"""Kata 9 (after): the god object split into three cohesive classes -- validation has no side effect anymore."""


class EmailValidator:  # => SRP: validation, and only validation -- no shared mutable state with anything else
    def is_valid(self, email: str) -> bool:
        return "@" in email


class UserRepository:  # => SRP: persistence, and only persistence
    def __init__(self) -> None:
        self.database: list[str] = []

    def save(self, email: str) -> None:
        self.database.append(email)


class WelcomeNotifier:  # => SRP: notification, and only notification
    def __init__(self) -> None:
        self.notifications: list[str] = []

    def notify(self, email: str) -> None:
        self.notifications.append(f"welcome {email}")


validator = EmailValidator()
repository = UserRepository()
notifier = WelcomeNotifier()

email = "not-an-email"
if validator.is_valid(email):  # a PURE check -- no side effect, safe to call as many times as needed
    repository.save(email)
    notifier.notify(email)

print(repository.database)  # never persisted -- the invalid email correctly never reached save()
