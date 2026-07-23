"""Kata 1 (before): SRP violation -- pricing and notification mixed in one class."""


class ReportGenerator:
    def __init__(self) -> None:
        self.email_log: list[str] = []

    def total(self, amounts: list[float]) -> float:
        result = sum(amounts)
        self.email_log.append(f"emailed total {result}")  # SMELL: a "total" getter has a notification side effect
        return result


report = ReportGenerator()
print(report.total([10.0, 20.0]))
print(report.total([10.0, 20.0]))  # called again, e.g. to redisplay -- but this ALSO re-sends an email
print(report.email_log)
