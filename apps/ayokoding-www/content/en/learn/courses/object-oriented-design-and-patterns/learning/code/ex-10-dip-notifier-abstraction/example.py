"""Example 10: Depend on a Notifier Protocol, Not a Concrete Sender."""

from typing import Protocol  # => Protocol declares the abstraction AlertService depends on


class Notifier(Protocol):  # => the ABSTRACTION every concrete sender must match
    # => both high-level AlertService and every low-level sender depend on THIS
    def send(self, message: str) -> str:  # => the one method any notifier must provide
        ...  # => Protocol methods have no body -- a structural contract only


class EmailNotifier:  # => one concrete, low-level detail among several possible ones
    def send(self, message: str) -> str:  # => satisfies Notifier structurally
        return f"email: {message}"  # => a real, honest implementation


class SMSNotifier:  # => a SECOND concrete detail, swapped in with zero service edits
    def send(self, message: str) -> str:  # => satisfies Notifier structurally
        return f"sms: {message}"  # => a real, honest implementation


class AlertService:  # => the HIGH-level policy -- depends on Notifier, not a sender
    def __init__(
        self,
        notifier: Notifier,
        # => names the PROTOCOL only -- no concrete sender class is visible here
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.notifier = notifier  # => held as a collaborator, injected from outside

    def alert(self, message: str) -> str:  # => defines the alert() method
        return self.notifier.send(message)  # => the DIRECTION of dependency: AlertService -> Notifier, never reversed


via_email: AlertService = AlertService(EmailNotifier())  # => one concrete sender chosen
via_sms: AlertService = AlertService(SMSNotifier())  # => a DIFFERENT sender, same service

print(via_email.alert("server down"))  # => routed through EmailNotifier
print(via_sms.alert("server down"))  # => routed through SMSNotifier, zero service edits
# => Output: email: server down
# => sms: server down
# => Swapping `EmailNotifier` for `SMSNotifier` never touches a single line inside `AlertService`
