"""Kata 1 (after): SRP -- pricing and notification separated into two classes."""


class ReportCalculator:
    def total(self, amounts: list[float]) -> float:
        return sum(amounts)  # a PURE calculation -- no side effect, safe to call any number of times


class ReportMailer:
    def __init__(self) -> None:
        self.email_log: list[str] = []

    def send(self, total: float) -> None:
        self.email_log.append(f"emailed total {total}")


calculator = ReportCalculator()
mailer = ReportMailer()
total = calculator.total([10.0, 20.0])
print(total)
print(calculator.total([10.0, 20.0]))  # calling total() again is now SAFE -- no side effect
mailer.send(total)  # sending is now an EXPLICIT, separate action
print(mailer.email_log)
