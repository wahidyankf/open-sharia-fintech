"""Example 10: pytest verification for Depend on a Notifier Protocol, Not a Concrete Sender."""

import inspect

from example import AlertService, EmailNotifier, SMSNotifier


def test_alert_service_source_never_names_a_concrete_sender() -> None:
    source: str = inspect.getsource(AlertService)  # => reads AlertService's own source text, nothing else
    assert "EmailNotifier" not in source  # => the concrete sender never appears here
    assert "SMSNotifier" not in source  # => neither does the second one


def test_swapping_the_notifier_needs_no_service_edit() -> None:
    via_email: AlertService = AlertService(EmailNotifier())
    via_sms: AlertService = AlertService(SMSNotifier())  # => swapped, same AlertService
    assert via_email.alert("server down") == "email: server down"
    assert via_sms.alert("server down") == "sms: server down"


# => Run: pytest -- Output: 2 passed
