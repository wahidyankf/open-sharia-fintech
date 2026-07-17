"""Kata 5 (before): DIP violation -- ReportService hard-codes a concrete repository, so it cannot be tested with a fake."""


class MySQLRepository:
    def fetch_total(self) -> float:
        raise ConnectionError("no real database available in this environment")  # simulates an unavailable real DB


class ReportService:
    def __init__(self) -> None:
        self.repository = MySQLRepository()  # SMELL: hard-coded concrete dependency, constructed INSIDE __init__

    def total(self) -> float:
        return self.repository.fetch_total()


service = ReportService()
try:
    print(service.total())  # there is no way to substitute a fake repository from outside
except ConnectionError as error:
    print(f"crashed: {error}")
