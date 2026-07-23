"""Example 16: High Cohesion: Split a Mixed-Concern Class."""


class UserAccount:  # => AFTER the split: every method touches ONLY account fields
    def __init__(self, username: str, email: str) -> None:  # => the constructor
        self.username = username  # => account-owned state
        self.email = email  # => account-owned state

    def display_name(self) -> str:  # => reads ONLY UserAccount's own fields
        return f"@{self.username}"  # => never touches anything email-server related


class EmailSender:  # => AFTER the split: every method touches ONLY email fields
    def __init__(self, smtp_host: str) -> None:  # => the constructor
        self.smtp_host = smtp_host  # => email-owned state, unrelated to accounts

    def send(self, to: str, subject: str) -> str:  # => reads ONLY EmailSender's fields
        return f"sent via {self.smtp_host} to {to}: {subject}"  # => stays in its lane


account: UserAccount = UserAccount("alice", "alice@example.com")  # => constructs account
sender: EmailSender = EmailSender("smtp.example.com")  # => constructs sender, separately

print(account.display_name())  # => a pure account concern
print(sender.send(account.email, "Welcome"))  # => a pure email concern, using account data
# => Output: @alice
# => sent via smtp.example.com to alice@example.com: Welcome
# => Before the split, one class mixed account fields with SMTP fields -- every method touched only HALF its own state
