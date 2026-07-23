"""Example 56: Dependency Inversion Using an abc.ABC Abstract Base."""

import abc  # => imports the abc module


class NotificationSender(abc.ABC):  # => the ABSTRACTION -- owned by the HIGH-level policy
    @abc.abstractmethod
    def send(self, message: str) -> str:  # => no body -- required by every concrete sender
        ...  # => the ellipsis stub -- concrete senders below fill this in


class EmailSender(NotificationSender):  # => a LOW-level detail -- implements the abstraction
    def send(self, message: str) -> str:  # => defines the send() method
        return f"email: {message}"  # => returns this value to the caller


class SmsSender(NotificationSender):  # => a DIFFERENT low-level detail, same abstraction
    def send(self, message: str) -> str:  # => defines the send() method
        return f"sms: {message}"  # => returns this value to the caller


class IncompleteSender(NotificationSender):  # => deliberately OMITS send() -- for the next check
    pass  # => an intentionally empty body


class Notifier:  # => the HIGH-level policy -- depends ONLY on the abstraction, not on details
    def __init__(self, sender: NotificationSender) -> None:  # => the constructor
        self.sender = sender  # => held as the abstraction, never a concrete type

    def notify(self, message: str) -> str:  # => defines the notify() method
        return self.sender.send(message)  # => calls THROUGH the abstraction, never a detail


notifier: Notifier = Notifier(EmailSender())  # => wired to one concrete detail
print(notifier.notify("build failed"))  # => Notifier itself never mentions "email" anywhere
# => Output: email: build failed

notifier.sender = SmsSender()  # => SWAPPED to a different detail, no Notifier class edit
print(notifier.notify("build failed"))  # => the SAME notify() call-site, a different detail underneath
# => Output: sms: build failed

try:  # => the block below is expected to raise
    IncompleteSender()  # type: ignore  # => never implemented send() -- ABC blocks instantiation
except TypeError as exc:  # => catches the TypeError raised above
    print(type(exc).__name__)  # => confirms the exact exception type raised
# => Output: TypeError
# => `abc.ABC` enforces that every concrete subtype implements the FULL abstraction before it can even be constructed
