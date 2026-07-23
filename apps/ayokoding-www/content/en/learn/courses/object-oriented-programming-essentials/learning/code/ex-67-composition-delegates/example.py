"""Example 67: A Service Delegates to a Logger Collaborator."""

from typing import Protocol  # => imports Protocol from typing


class SupportsLog(Protocol):  # => the structural contract Service actually depends on
    def log(
        self, message: str
    ) -> str: ...  # => no body -- Logger and SilentLogger each supply one


class Logger:  # => begins the Logger class body
    def log(self, message: str) -> str:  # => the default collaborator behavior
        return f"[LOG] {message}"  # => returns this value to the caller


class SilentLogger:  # => unrelated to Logger -- satisfies SupportsLog structurally, not by inheritance
    def log(self, message: str) -> str:  # => same method NAME, deliberately swappable
        return ""  # => discards the message instead of formatting it


class Service:  # => begins the Service class body
    def __init__(
        self, logger: SupportsLog
    ) -> None:  # => typed against the PROTOCOL, not a class
        self.logger = logger  # => HOLDS a collaborator -- does not inherit from it

    def run(self) -> str:  # => defines the run() method
        return self.logger.log(
            "service ran"
        )  # => delegates the actual work to the collaborator


loud: Service = Service(Logger())  # => constructs loud
quiet: Service = Service(SilentLogger())  # => structurally compatible, accepted cleanly
print(
    f"{loud.run()!r} | {quiet.run()!r}"
)  # => swapping the collaborator changed the observed behavior
# => Output: '[LOG] service ran' | ''
# => `Service.run()` never knows or cares which `log()` implementation it holds
