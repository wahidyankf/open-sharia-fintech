"""Example 76: Splitting a Two-Responsibility Class into Composed Collaborators."""


class ReportGenerator:  # => AFTER the refactor -- each collaborator owns ONE responsibility
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.formatter: Formatter = Formatter()  # => composed, not inherited
        self.sender: Sender = Sender()  # => stores sender on this instance

    def send_report(self, data: str) -> str:  # => defines the send_report() method
        formatted: str = self.formatter.format(data)  # => delegates FORMATTING entirely
        return self.sender.send(formatted)  # => delegates SENDING entirely


class Formatter:  # => responsibility #1: turning raw data into a formatted string
    def format(self, data: str) -> str:  # => defines the format() method
        return f"[REPORT] {data}"  # => returns this value to the caller


class Sender:  # => responsibility #2: delivering an already-formatted string
    def send(self, formatted: str) -> str:  # => defines the send() method
        return f"sent: {formatted}"  # => returns this value to the caller


generator: ReportGenerator = ReportGenerator()  # => constructs generator
print(
    generator.send_report("Q3 numbers")
)  # => the same overall behavior, now composed of two units
# => Output: sent: [REPORT] Q3 numbers
# => `Formatter` and `Sender` can each be tested, understood, and changed independently
