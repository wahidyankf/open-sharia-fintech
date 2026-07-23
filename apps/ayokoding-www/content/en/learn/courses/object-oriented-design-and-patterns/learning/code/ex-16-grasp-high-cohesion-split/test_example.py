"""Example 16: pytest verification for High Cohesion: Split a Mixed-Concern Class."""

from example import EmailSender, UserAccount


def test_user_account_has_no_email_infrastructure_fields() -> None:
    account: UserAccount = UserAccount("alice", "alice@example.com")
    assert not hasattr(account, "smtp_host")  # => never carries the other class's state
    assert not hasattr(UserAccount, "send")  # => never carries the other class's method


def test_email_sender_has_no_account_fields() -> None:
    sender: EmailSender = EmailSender("smtp.example.com")
    assert not hasattr(sender, "username")  # => never carries the other class's state
    assert not hasattr(EmailSender, "display_name")  # => never carries the other method


def test_each_class_still_produces_correct_output() -> None:
    account: UserAccount = UserAccount("alice", "alice@example.com")
    sender: EmailSender = EmailSender("smtp.example.com")
    assert account.display_name() == "@alice"
    assert sender.send(account.email, "Welcome") == ("sent via smtp.example.com to alice@example.com: Welcome")  # => the two cohesive classes still cooperate correctly


# => Run: pytest -- Output: 3 passed
